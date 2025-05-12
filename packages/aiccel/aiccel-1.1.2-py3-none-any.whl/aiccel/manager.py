import json
import re
import asyncio
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import aiohttp

from .agent import Agent
from .tools import ToolRegistry
from .logger import AILogger

class AgentManager:
    """Manages multiple specialized agents and routes tasks to them"""
    def __init__(self, llm_provider, agents=None, verbose=False, instructions: str = None, 
                 log_file: Optional[str] = None, structured_logging: bool = False, 
                 fallback_providers: Optional[List] = None):
        self.provider = llm_provider
        self.agents = {}
        self.history = []
        self.verbose = verbose
        self.instructions = instructions or (
            "Route queries to the most appropriate agent based on their expertise and available tools. "
            "Consider the query's intent, required knowledge, and tool capabilities."
        )
        self.logger = AILogger(
            name="AgentManager",
            verbose=verbose,
            log_file=log_file,
            structured_logging=structured_logging
        )
        self.fallback_providers = fallback_providers or []
        self.http_session = None
        self.tool_cache = {}  # Shared cache for tool outputs
        self.semaphore = asyncio.Semaphore(2)  # Reduced to 2 for API rate limit stability

        if agents:
            if isinstance(agents, list):
                for agent in agents:
                    self.add_agent(
                        name=agent.name,
                        agent=agent,
                        description=f"Agent specialized in {agent.name} tasks"
                    )
            elif isinstance(agents, dict):
                for name, agent_info in agents.items():
                    if isinstance(agent_info, dict):
                        self.add_agent(
                            name=name,
                            agent=agent_info.get("agent"),
                            description=agent_info.get("description", f"Agent specialized in {name} tasks")
                        )
                    else:
                        self.add_agent(
                            name=name,
                            agent=agent_info,
                            description=f"Agent specialized in {name} tasks"
                        )

    async def __aenter__(self):
        self.http_session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.http_session:
            await self.http_session.close()

    @classmethod
    def from_agents(cls, agents: List[Agent], llm_provider=None, verbose=False, 
                    instructions: str = None, log_file: Optional[str] = None, 
                    structured_logging: bool = False, 
                    fallback_providers: Optional[List] = None) -> 'AgentManager':
        if not llm_provider and agents:
            llm_provider = agents[0].provider
        manager = cls(
            llm_provider=llm_provider,
            verbose=verbose,
            instructions=instructions,
            log_file=log_file,
            structured_logging=structured_logging,
            fallback_providers=fallback_providers
        )
        for agent in agents:
            manager.add_agent(
                name=agent.name,
                agent=agent,
                description=f"Agent specialized in {agent.name} tasks"
            )
        return manager

    def set_verbose(self, verbose: bool = True) -> 'AgentManager':
        self.verbose = verbose
        self.logger.verbose = verbose
        for name, info in self.agents.items():
            info["agent"].set_verbose(verbose)
        self.logger.info(f"Verbose mode set to: {verbose}")
        return self

    def set_instructions(self, instructions: str) -> 'AgentManager':
        self.instructions = instructions
        self.logger.info(f"Updated routing instructions: {instructions[:50]}...")
        return self

    def add_agent(self, name: str, agent: Agent, description: str) -> 'AgentManager':
        self.agents[name] = {
            "agent": agent,
            "description": description
        }
        agent.name = name
        agent.set_verbose(self.verbose)
        # Inject shared cache into agent
        agent.tool_cache = self.tool_cache
        self.logger.info(f"Added agent: {name} - {description}")
        return self

    def _build_agent_descriptions(self) -> str:
        agent_descriptions = []
        for name, info in self.agents.items():
            tool_info = ""
            if agent := info["agent"]:
                if hasattr(agent, "tool_registry") and agent.tool_registry:
                    tools = agent.tool_registry.get_all()
                    if tools:
                        tool_names = [t.name for t in tools]
                        tool_info = f" (Tools: {', '.join(tool_names)})"
            agent_descriptions.append(f"- {name}: {info['description']}{tool_info}")
        return "\n".join(agent_descriptions)

    def _select_default_agent(self) -> str:
        preferred_agents = ["general_expert", "search_expert"]
        for agent in preferred_agents:
            if agent in self.agents:
                return agent
        return list(self.agents.keys())[0] if self.agents else None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    def route(self, query: str) -> Dict[str, Any]:
        trace_id = self.logger.trace_start("route_query", {"query": query[:100] + "..." if len(query) > 100 else query})
        if not self.agents:
            self.logger.error("No agents available to handle query")
            self.logger.trace_end(trace_id, {"error": "No agents available"})
            raise ValueError("No agents available")
        if len(self.agents) == 1:
            agent_name = list(self.agents.keys())[0]
            agent = self.agents[agent_name]["agent"]
            self.logger.info(f"Only one agent available, using: {agent_name}")
            try:
                result = agent.run(query)
                result["agent_used"] = agent_name
                self.history.append({
                    "query": query,
                    "agent": agent_name,
                    "response": result["response"],
                    "timestamp": datetime.now().isoformat()
                })
                self.logger.trace_step(trace_id, "agent_execution", {
                    "agent": agent_name,
                    "response": result["response"][:100] + "..." if len(result["response"]) > 100 else result["response"]
                })
                self.logger.trace_end(trace_id, result)
                return result
            except Exception as e:
                self.logger.trace_error(trace_id, e, f"Agent {agent_name} execution failed")
                raise Exception(f"Single agent {agent_name} failed: {str(e)}")
        agent_descriptions_text = self._build_agent_descriptions()
        routing_prompt = (
            f"Instructions: {self.instructions}\n\n"
            f"Query: {query}\n\n"
            "Available agents:\n"
            f"{agent_descriptions_text}\n\n"
            "Select the most appropriate agent to handle this query based on their expertise and tools. "
            "You MUST return only the agent name as a plain string (e.g., 'weather_expert'). "
            "Do not include any additional text, explanations, or formatting."
        )
        self.logger.trace_step(trace_id, "build_routing_prompt", {"prompt": routing_prompt[:200] + "..." if len(routing_prompt) > 200 else routing_prompt})
        selected_agent = None
        providers = [self.provider] + self.fallback_providers
        for provider in providers:
            try:
                self.logger.info(f"Attempting routing with provider: {type(provider).__name__}")
                selected_agent = provider.generate(routing_prompt).strip()
                self.logger.trace_step(trace_id, "routing_decision", {
                    "provider": type(provider).__name__,
                    "selected_agent": selected_agent
                })
                if selected_agent in self.agents:
                    break
                self.logger.warning(f"Invalid agent selected: {selected_agent}, retrying with next provider")
                selected_agent = None
            except Exception as e:
                self.logger.trace_error(trace_id, e, f"Routing with provider {type(provider).__name__} failed")
                continue
        if not selected_agent:
            self.logger.error("Failed to select a valid agent, falling back to default agent")
            selected_agent = self._select_default_agent()
            self.logger.trace_step(trace_id, "fallback_to_default_agent", {"selected_agent": selected_agent})
        agent = self.agents[selected_agent]["agent"]
        self.logger.info(f"Routing query to agent: {selected_agent}")
        try:
            result = agent.run(query)
            result["agent_used"] = selected_agent
            self.history.append({
                "query": query,
                "agent": selected_agent,
                "response": result["response"],
                "timestamp": datetime.now().isoformat()
            })
            self.logger.trace_step(trace_id, "agent_execution", {
                "agent": selected_agent,
                "response": result["response"][:100] + "..." if len(result["response"]) > 100 else result["response"]
            })
            self.logger.trace_end(trace_id, result)
            return result
        except Exception as e:
            self.logger.trace_error(trace_id, e, f"Agent {selected_agent} execution failed")
            raise Exception(f"Agent {selected_agent} failed: {str(e)}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def route_async(self, query: str) -> Dict[str, Any]:
        trace_id = self.logger.trace_start("route_query_async", {"query": query[:100] + "..." if len(query) > 100 else query})
        if not self.agents:
            self.logger.error("No agents available to handle query")
            self.logger.trace_end(trace_id, {"error": "No agents available"})
            raise ValueError("No agents available")
        if len(self.agents) == 1:
            agent_name = list(self.agents.keys())[0]
            agent = self.agents[agent_name]["agent"]
            self.logger.info(f"Only one agent available, using: {agent_name}")
            try:
                result = await agent.run_async(query)
                result["agent_used"] = agent_name
                self.history.append({
                    "query": query,
                    "agent": agent_name,
                    "response": result["response"],
                    "timestamp": datetime.now().isoformat()
                })
                self.logger.trace_step(trace_id, "agent_execution", {
                    "agent": agent_name,
                    "response": result["response"][:100] + "..." if len(result["response"]) > 100 else result["response"]
                })
                self.logger.trace_end(trace_id, result)
                return result
            except Exception as e:
                self.logger.trace_error(trace_id, e, f"Agent {agent_name} execution failed")
                raise Exception(f"Single agent {agent_name} failed: {str(e)}")
        agent_descriptions_text = self._build_agent_descriptions()
        routing_prompt = (
            f"Instructions: {self.instructions}\n\n"
            f"Query: {query}\n\n"
            "Available agents:\n"
            f"{agent_descriptions_text}\n\n"
            "Select the most appropriate agent to handle this query based on their expertise and tools. "
            "You MUST return only the agent name as a plain string (e.g., 'weather_expert'). "
            "Do not include any additional text, explanations, or formatting."
        )
        self.logger.trace_step(trace_id, "build_routing_prompt", {"prompt": routing_prompt[:200] + "..." if len(routing_prompt) > 200 else routing_prompt})
        selected_agent = None
        providers = [self.provider] + self.fallback_providers
        for provider in providers:
            try:
                self.logger.info(f"Attempting async routing with provider: {type(provider).__name__}")
                selected_agent = (await provider.generate_async(routing_prompt)).strip()
                self.logger.trace_step(trace_id, "routing_decision", {
                    "provider": type(provider).__name__,
                    "selected_agent": selected_agent
                })
                if selected_agent in self.agents:
                    break
                self.logger.warning(f"Invalid agent selected: {selected_agent}, retrying with next provider")
                selected_agent = None
            except Exception as e:
                self.logger.trace_error(trace_id, e, f"Async routing with provider {type(provider).__name__} failed")
                continue
        if not selected_agent:
            self.logger.error("Failed to select a valid agent, falling back to default agent")
            selected_agent = self._select_default_agent()
            self.logger.trace_step(trace_id, "fallback_to_default_agent", {"selected_agent": selected_agent})
        agent = self.agents[selected_agent]["agent"]
        self.logger.info(f"Routing query to agent: {selected_agent}")
        try:
            result = await agent.run_async(query)
            result["agent_used"] = selected_agent
            self.history.append({
                "query": query,
                "agent": selected_agent,
                "response": result["response"],
                "timestamp": datetime.now().isoformat()
            })
            self.logger.trace_step(trace_id, "agent_execution", {
                "agent": selected_agent,
                "response": result["response"][:100] + "..." if len(result["response"]) > 100 else result["response"]
            })
            self.logger.trace_end(trace_id, result)
            return result
        except Exception as e:
            self.logger.trace_error(trace_id, e, f"Agent {selected_agent} execution failed")
            raise Exception(f"Agent {selected_agent} failed: {str(e)}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    def collaborate(self, query: str, max_agents: int = 5, agent_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        trace_id = self.logger.trace_start("collaborate", {
            "query": query[:100] + "..." if len(query) > 100 else query,
            "max_agents": max_agents
        })
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    self.collaborate_async(query, max_agents, agent_ids)
                )
                self.logger.trace_end(trace_id, {
                    "response": result["response"][:100] + "..." if len(result["response"]) > 100 else result["response"],
                    "agents_used": result["agents_used"]
                })
                return result
            finally:
                loop.close()
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Synchronous collaboration failed")
            raise Exception(f"Collaboration failed: {str(e)}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def collaborate_async(self, query: str, max_agents: int = 5, agent_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        trace_id = self.logger.trace_start("collaborate_async", {
            "query": query[:100] + "..." if len(query) > 100 else query,
            "max_agents": max_agents
        })

        async with self:  # Manage HTTP session
            if not self.agents:
                self.logger.error("No agents available for collaboration")
                self.logger.trace_end(trace_id, {"error": "No agents available"})
                raise ValueError("No agents available")

            # Dynamic agent selection based on query
            required_agents = []
            if "weather" in query.lower():
                required_agents.append("weather_expert")
            if any(keyword in query.lower() for keyword in ["itinerary", "plan", "trip"]):
                required_agents.append("itinerary_expert")
            if any(keyword in query.lower() for keyword in ["attractions", "events", "activities"]):
                required_agents.append("search_expert")

            if agent_ids:
                selected_agents = [aid for aid in agent_ids if aid in self.agents and aid in required_agents][:max_agents]
            else:
                selected_agents = [aid for aid in required_agents if aid in self.agents][:max_agents]

            if not selected_agents:
                selected_agents = list(self.agents.keys())[:max_agents]
            self.logger.info(f"Selected agents for async collaboration: {', '.join(selected_agents)}")
            self.logger.trace_step(trace_id, "agents_selected", {"selected_agents": selected_agents})

            # Dynamic timeouts based on agent tools
            agent_timeouts = {}
            for agent_name in selected_agents:
                agent = self.agents[agent_name]["agent"]
                timeout = 30.0  # Default
                if hasattr(agent, "tool_registry") and agent.tool_registry:
                    tools = agent.tool_registry.get_all()
                    if any(tool.name in ["search", "get_weather"] for tool in tools):
                        timeout = 45.0  # Longer for API-heavy agents
                agent_timeouts[agent_name] = timeout

            results = []
            tasks = []

            async def run_agent_with_semaphore(agent_name: str, agent: Agent, query: str) -> Dict[str, Any]:
                async with self.semaphore:
                    start_time = asyncio.get_event_loop().time()
                    try:
                        result = await asyncio.wait_for(
                            self._run_agent_async_with_error_handling(agent, agent_name, query, trace_id),
                            timeout=agent_timeouts[agent_name]
                        )
                        # Cache tool output
                        if result.get("tool_used") and result.get("tool_output"):
                            cache_key = f"{result['tool_used']}:{json.dumps(result['tool_output'], sort_keys=True)}"
                            self.tool_cache[cache_key] = result["tool_output"]
                        normalized_result = {
                            "agent": agent_name,
                            "agent_used": agent_name,
                            "response": result.get("response", "No response")[:1000],  # Truncate for synthesis
                            "tool_used": result.get("tool_used"),
                            "tool_output": result.get("tool_output")
                        }
                        self.logger.debug(f"Agent {agent_name} completed in {asyncio.get_event_loop().time() - start_time:.2f}s")
                        return normalized_result
                    except asyncio.TimeoutError:
                        self.logger.error(f"Agent {agent_name} timed out after {agent_timeouts[agent_name]}s")
                        return {
                            "agent": agent_name,
                            "agent_used": agent_name,
                            "response": f"Error: Agent timed out",
                            "tool_used": None,
                            "tool_output": None
                        }
                    except Exception as e:
                        self.logger.trace_error(trace_id, e, f"Agent {agent_name} failed")
                        return {
                            "agent": agent_name,
                            "agent_used": agent_name,
                            "response": f"Error: Agent {agent_name} failed: {str(e)}",
                            "tool_used": None,
                            "tool_output": None
                        }

            # Schedule agent tasks
            for agent_name in selected_agents:
                agent = self.agents[agent_name]["agent"]
                self.logger.info(f"Scheduling async agent: {agent_name}")
                tasks.append(run_agent_with_semaphore(agent_name, agent, query))

            # Run tasks in parallel and start synthesis early
            synthesis_prompt_parts = [
                "You are a travel itinerary synthesizer. Combine agent outputs into a single, concise, and coherent response for the query. "
                "Avoid redundancy, prioritize reliable data, and disregard erroneous responses unless they provide useful partial information. "
                f"Query: {query}\n\nAgent Responses:\n"
            ]
            results = []

            # Process tasks as they complete to build synthesis prompt incrementally
            for future in asyncio.as_completed(tasks):
                result = await future
                results.append(result)
                agent_name = result["agent"]
                response = result["response"][:1000]  # Truncate early
                synthesis_prompt_parts.append(f"Agent {agent_name}:\n{response}\n\n")
                self.logger.trace_step(trace_id, f"agent_{agent_name}_execution", {
                    "response": response[:100] + "..." if len(response) > 100 else response
                })

            synthesis_prompt = "".join(synthesis_prompt_parts)
            self.logger.trace_step(trace_id, "build_synthesis_prompt", {
                "prompt": synthesis_prompt[:200] + "..." if len(synthesis_prompt) > 200 else synthesis_prompt
            })

            # Parallel synthesis with fallback providers
            async def try_synthesis(provider, prompt: str) -> Optional[str]:
                try:
                    self.logger.info(f"Attempting async synthesis with provider: {type(provider).__name__}")
                    response = await provider.generate_async(prompt)
                    self.logger.trace_step(trace_id, f"synthesis_{type(provider).__name__}", {
                        "response": response[:100] + "..." if len(response) > 100 else response
                    })
                    return response
                except Exception as e:
                    self.logger.trace_error(trace_id, e, f"Synthesis with {type(provider).__name__} failed")
                    return None

            synthesis_tasks = [try_synthesis(provider, synthesis_prompt) for provider in [self.provider] + self.fallback_providers]
            final_response = None
            for future in asyncio.as_completed(synthesis_tasks):
                response = await future
                if response:
                    final_response = response
                    break

            if not final_response:
                final_response = "No valid responses from agents"
                self.logger.error("All synthesis attempts failed")

            final_result = {
                "response": final_response,
                "agent_results": results,
                "agents_used": selected_agents
            }

            self.history.append({
                "query": query,
                "agents": selected_agents,
                "response": final_response,
                "timestamp": datetime.now().isoformat()
            })

            self.logger.trace_end(trace_id, {
                "response": final_response[:100] + "..." if len(final_response) > 100 else final_response,
                "agents_used": selected_agents
            })
            return final_result

    async def _run_agent_async_with_error_handling(self, agent: Agent, agent_name: str, query: str, trace_id: int) -> Dict[str, Any]:
        try:
            result = await agent.run_async(query)
            normalized_result = {
                "agent": agent_name,
                "agent_used": agent_name,
                "response": result.get("response", "No response"),
                "tool_used": result.get("tool_used"),
                "tool_output": result.get("tool_output")
            }
            self.logger.trace_step(trace_id, f"agent_{agent_name}_execution", {
                "agent": agent_name,
                "response": normalized_result["response"][:100] + "..." if len(normalized_result["response"]) > 100 else normalized_result["response"]
            })
            return normalized_result
        except Exception as e:
            self.logger.trace_error(trace_id, e, f"Agent {agent_name} execution failed")
            return {
                "agent": agent_name,
                "agent_used": agent_name,
                "response": f"Error: Agent {agent_name} failed: {str(e)}",
                "tool_used": None,
                "tool_output": None
            }