from abc import ABC, abstractmethod
import json
import requests
import asyncio
import re
import os
from typing import Dict, Any, Callable, List, Optional, Union, Set, Pattern
from urllib.parse import quote_plus
from .providers import LLMProvider
from .embeddings import EmbeddingProvider, OpenAIEmbeddingProvider
from chromadb import PersistentClient
from chromadb.utils import embedding_functions
import PyPDF2
from textsplitter import TextSplitter
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Tool:
    """Enhanced base class for tools with intelligent relevance assessment"""
    def __init__(self, 
                 name: str, 
                 description: str, 
                 function: Callable,
                 llm_provider: Optional[LLMProvider] = None,
                 capability_keywords: Optional[List[str]] = None,
                 detection_patterns: Optional[List[Union[str, Pattern]]] = None,
                 detection_threshold: float = 0.5):
        self.name = name
        self.description = description
        self.function = function
        self.llm_provider = llm_provider
        self.capability_keywords = set(capability_keywords or [])
        
        self.detection_patterns = []
        if detection_patterns:
            for pattern in detection_patterns:
                if isinstance(pattern, str):
                    self.detection_patterns.append(re.compile(pattern, re.IGNORECASE))
                else:
                    self.detection_patterns.append(pattern)
                    
        self.detection_threshold = detection_threshold
        self.example_usages = []
    
    def set_llm_provider(self, provider: LLMProvider) -> 'Tool':
        self.llm_provider = provider
        return self
    
    def add_capability(self, keyword: str) -> 'Tool':
        self.capability_keywords.add(keyword)
        return self
    
    def add_pattern(self, pattern: Union[str, Pattern]) -> 'Tool':
        if isinstance(pattern, str):
            self.detection_patterns.append(re.compile(pattern, re.IGNORECASE))
        else:
            self.detection_patterns.append(pattern)
        return self
    
    def add_example(self, example: Dict[str, Any]) -> 'Tool':
        self.example_usages.append(example)
        return self
        
    def execute(self, args: Dict[str, Any]) -> str:
        return self.function(args)
        
    async def execute_async(self, args: Dict[str, Any]) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.execute, args)
    
    def assess_relevance(self, query: str) -> float:
        if not self.llm_provider:
            score = 0.0
            query_lower = query.lower()
            for keyword in self.capability_keywords:
                if keyword.lower() in query_lower:
                    score += 0.3
                    break
            for pattern in self.detection_patterns:
                if pattern.search(query):
                    score += 0.7
                    break
            return min(score, 1.0)

        relevance_prompt = (
            f"Query: {query}\n\n"
            f"Tool: {self.name}\n"
            f"Description: {self.description}\n\n"
            "Determine how relevant this tool is for the query on a scale from 0 to 1, where 0 is not relevant and 1 is highly relevant. "
            "Return a single float value between 0 and 1."
        )
        try:
            response = self.llm_provider.generate(relevance_prompt)
            return float(response.strip())
        except (ValueError, Exception):
            return self._keyword_based_relevance(query)
    
    def _keyword_based_relevance(self, query: str) -> float:
        score = 0.0
        query_lower = query.lower()
        for keyword in self.capability_keywords:
            if keyword.lower() in query_lower:
                score += 0.3
                break
        for pattern in self.detection_patterns:
            if pattern.search(query):
                score += 0.7
                break
        return min(score, 1.0)
    
    def is_relevant(self, query: str) -> bool:
        return self.assess_relevance(query) >= self.detection_threshold
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "capabilities": list(self.capability_keywords),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    
    def get_format_instructions(self) -> str:
        instructions = f"To use the {self.name} tool, format like this:\n"
        instructions += f'[TOOL]{{"name": "{self.name}", "args": {{...}}}}[/TOOL]\n\n'
        
        if self.example_usages:
            instructions += "Examples:\n"
            for example in self.example_usages:
                instructions += f"[TOOL]{json.dumps(example)}[/TOOL]\n"
                
        return instructions

class SearchTool(Tool):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        search_patterns = [
            r"(?:search|find|look up|google|research|information about|tell me about|what is|who is|where is|when|how to)\s+(.+)",
            r"(?:latest|news|information|details)\s+(?:about|on|regarding)\s+(.+)"
        ]
        capabilities = [
            "search", "find", "lookup", "information", "research", 
            "facts", "news", "current events", "details", "data"
        ]
        super().__init__(
            name="search",
            description="Search the web for current information on a topic",
            function=self._search,
            capability_keywords=capabilities,
            detection_patterns=search_patterns,
            detection_threshold=0.3
        )
        self.add_example({"name": "search", "args": {"query": "current climate news"}})
        self.add_example({"name": "search", "args": {"query": "who is the CEO of OpenAI"}})
    
    def _search(self, args: Dict[str, Any]) -> str:
        query = None
        for param_name in ["query", "q", "search", "text", "input", "searchQuery"]:
            if param_name in args and args[param_name]:
                query = args[param_name]
                break
        
        if not query:
            return "Error: No search query provided. Please specify what you want to search for."
        
        if not self.api_key:
            return "Error: Search API key is not configured"
            
        try:
            return self._search_with_serper(query)
        except Exception as e:
            error_message = str(e)
            if "401" in error_message:
                return "Error: Invalid API key or authentication failed"
            elif "429" in error_message:
                return "Error: API rate limit exceeded. Please try again later."
            else:
                return f"Error performing search: {error_message}. Please try with a different query."
    
    def _search_with_serper(self, query: str) -> str:
        url = "https://google.serper.dev/search"
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        payload = {
            'q': query,
            'num': 15
        }
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        result = f"Search results for '{query}':\n\n"
        if 'organic' in data:
            for i, item in enumerate(data['organic'][:5], 1):
                title = item.get('title', 'No title')
                link = item.get('link', 'No link')
                snippet = item.get('snippet', 'No description available')
                result += f"{i}. {title}\nURL: {link}\nDescription: {snippet}\n\n"
        if 'knowledgeGraph' in data:
            kg = data['knowledgeGraph']
            title = kg.get('title', '')
            description = kg.get('description', '')
            if title and description:
                result += f"Knowledge Graph: {title} - {description}\n\n"
        return result.strip()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "capabilities": list(self.capability_keywords),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }

class WeatherTool(Tool):
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("OpenWeatherMap API key is required for the WeatherTool")
        self.api_key = api_key
        weather_patterns = [
            r"(?:weather|temperature|forecast|climate|rain|sunny|cloudy|precipitation|humidity)\s+(?:in|at|for|of)\s+([A-Za-z\s,]+)",
            r"(?:how|what)(?:'s| is) the (?:weather|temperature|forecast|climate|humidity)\s+(?:in|at|for|of|like)\s+([A-Za-z\s,]+)",
            r"is it (?:raining|sunny|cloudy|hot|cold|warm|humid|snowing)\s+(?:in|at)\s+([A-Za-z\s,]+)"
        ]
        capabilities = [
            "weather", "temperature", "forecast", "climate", "rain", 
            "sunny", "cloudy", "snow", "precipitation", "humidity", 
            "wind", "atmospheric conditions"
        ]
        super().__init__(
            name="get_weather",
            description="Get current weather and forecast for a location",
            function=self._get_weather,
            capability_keywords=capabilities,
            detection_patterns=weather_patterns
        )
        self.add_example({"name": "get_weather", "args": {"location": "New York"}})
        self.add_example({"name": "get_weather", "args": {"location": "London, UK"}})
    
    def _get_weather(self, args: Dict[str, Any]) -> str:
        location = None
        for param_name in ["location", "city", "place", "loc"]:
            if param_name in args and args[param_name]:
                location = args[param_name]
                break
        if not location:
            return "Error: No location provided. Please specify a city or location."
        locations = self._parse_locations(location)
        if len(locations) > 1:
            weather_results = []
            for loc in locations:
                result = self._fetch_weather_for_location(loc)
                weather_results.append(result)
            return "\n\n".join(weather_results)
        else:
            return self._fetch_weather_for_location(locations[0])
    
    def _parse_locations(self, location_str: str) -> List[str]:
        if " and " in location_str.lower():
            locations = [loc.strip() for loc in location_str.lower().split(" and ")]
        elif "," in location_str:
            locations = [loc.strip() for loc in location_str.split(",")]
        else:
            locations = [location_str.strip()]
        return [loc for loc in locations if loc]
    
    def _fetch_weather_for_location(self, location: str) -> str:
        current_url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}&units=imperial"
        try:
            response = requests.get(current_url)
            response.raise_for_status()
            data = response.json()
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            weather_desc = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            city_name = data["name"]
            country = data["sys"]["country"]
            weather_report = (
                f"Weather in {city_name}, {country}:\n"
                f"• Temperature: {temp}°F (feels like {feels_like}°F)\n"
                f"• Conditions: {weather_desc.capitalize()}\n"
                f"• Humidity: {humidity}%\n"
                f"• Wind Speed: {wind_speed} mph"
            )
            if "clouds" in data:
                weather_report += f"\n• Cloud Cover: {data['clouds']['all']}%"
            if "rain" in data and "1h" in data["rain"]:
                weather_report += f"\n• Rainfall (last hour): {data['rain']['1h']} mm"
            if "snow" in data and "1h" in data["snow"]:
                weather_report += f"\n• Snowfall (last hour): {data['snow']['1h']} mm"
            try:
                forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={self.api_key}&units=imperial&cnt=8"
                forecast_response = requests.get(forecast_url)
                forecast_response.raise_for_status()
                forecast_data = forecast_response.json()
                if "list" in forecast_data and len(forecast_data["list"]) > 0:
                    weather_report += "\n\nForecast:"
                    for i, period in enumerate(forecast_data["list"][:3]):
                        time_str = period["dt_txt"].split(" ")[1][:5]
                        temp = period["main"]["temp"]
                        conditions = period["weather"][0]["description"].capitalize()
                        weather_report += f"\n• {time_str}: {temp}°F, {conditions}"
            except Exception:
                pass
            return weather_report
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return f"Error: Location '{location}' not found. Please check the spelling or try a different location."
            elif e.response.status_code == 401:
                return f"Error: Invalid API key. Please check your OpenWeatherMap API key."
            else:
                return f"Error fetching weather for {location}: HTTP error {e.response.status_code}"
        except requests.exceptions.ConnectionError:
            return f"Error: Could not connect to weather service. Please check your internet connection."
        except requests.exceptions.Timeout:
            return f"Error: Request to weather service timed out. Please try again later."
        except KeyError as e:
            return f"Error: Could not parse weather data for {location}. Missing data: {str(e)}"
        except Exception as e:
            return f"Error getting weather for {location}: {str(e)}"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "capabilities": list(self.capability_keywords),
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and country (e.g., 'London, UK' or multiple locations like 'Tokyo and New York')"
                    }
                },
                "required": ["location"]
            }
        }



class ToolRegistry:
    def __init__(self, llm_provider: Optional[LLMProvider] = None):
        self.tools = {}
        self.llm_provider = llm_provider
    
    def register(self, tool: Tool) -> 'ToolRegistry':
        self.tools[tool.name] = tool
        if self.llm_provider:
            tool.set_llm_provider(self.llm_provider)
        return self
    
    def register_all(self, tools: List[Tool]) -> 'ToolRegistry':
        for tool in tools:
            self.register(tool)
        return self
    
    def get(self, name: str) -> Optional[Tool]:
        return self.tools.get(name)
    
    def get_all(self) -> List[Tool]:
        return list(self.tools.values())
    
    def find_relevant_tools(self, query: str) -> List[Tool]:
        if not self.llm_provider or not self.tools:
            return [tool for tool in self.tools.values() if tool.is_relevant(query)]
        tool_descriptions = "\n".join(
            [f"- {tool.name}: {tool.description}" for tool in self.tools.values()]
        )
        selection_prompt = (
            f"Query: {query}\n\n"
            f"Available tools:\n{tool_descriptions}\n\n"
            "Select the most relevant tools for this query. Return a list of tool names in JSON format:\n"
            "```json\n[]\n```"
        )
        try:
            response = self.llm_provider.generate(selection_prompt)
            tool_names = json.loads(response.strip())
            return [self.tools[name] for name in tool_names if name in self.tools]
        except (json.JSONDecodeError, Exception):
            return [tool for tool in self.tools.values() if tool.is_relevant(query)]
    
    def find_most_relevant_tool(self, query: str) -> Optional[Tool]:
        tools = self.find_relevant_tools(query)
        if not tools:
            return None
        return max(tools, key=lambda tool: tool.assess_relevance(query))
    
    def get_tool_descriptions(self) -> str:
        if not self.tools:
            return "No tools available."
        descriptions = []
        for name, tool in self.tools.items():
            descriptions.append(f"- {name}: {tool.description}")
        return "\n".join(descriptions)
    
    def get_tool_specs(self) -> List[Dict[str, Any]]:
        return [tool.to_dict() for tool in self.tools.values()]

from aiccel.base_custom_tool import BaseCustomTool

class CustomTool(BaseCustomTool):
    def __init__(self, llm_provider, custom_param="default_value"):
        super().__init__(
            name="custom_tool",
            description="A custom tool for testing purposes",
            capability_keywords=["test", "custom"],
            detection_patterns=[r"test\s+(.+)"],
            parameters={"type": "object", "properties": {"input": {"type": "string"}}},
            examples=[{"name": "custom_tool", "args": {"input": "test input"}}],
            detection_threshold=0.5,
            llm_provider=llm_provider
        )
        self.custom_param = custom_param

    def _execute(self, args: Dict[str, Any]) -> str:
        input_value = args.get("input", "No input provided")
        return f"Custom tool executed with input: {input_value}, param: {self.custom_param}"





