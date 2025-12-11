"""
Tool definitions and mock API functions for the Travel Assistant.

This module defines:
1. Tool schemas for LLM tool calling
2. Mock API execution functions (weather, images, search)
3. Tool execution router
"""

import asyncio
import json
from typing import Any, Dict, List
from src.mock_apis.weather_mock import fetch_weather_forecast
from src.mock_apis.image_mock import fetch_city_images


# Tool schemas that LLM can call
TOOL_SCHEMAS = [
    {
        "name": "get_weather",
        "description": "Fetch current weather and 5-7 day forecast for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name (e.g., 'Paris', 'Tokyo', 'New York')"
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "get_images",
        "description": "Retrieve high-quality images of a city for visual context",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name to fetch images for"
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "web_search",
        "description": "Search the web for information about a city",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query about the city"
                }
            },
            "required": ["query"]
        }
    }
]


async def execute_tool(tool_name: str, tool_input: Dict[str, Any]) -> Any:
    """
    Execute a tool by name and return its result.
    
    This function demonstrates manual tool execution (Distinction 1).
    It's called from the node_execute_tools_parallel node.
    
    Args:
        tool_name: Name of the tool to execute
        tool_input: Dictionary of arguments for the tool
        
    Returns:
        Result from the tool (list, dict, or string)
        
    Raises:
        ValueError: If tool name is unknown
    """
    if tool_name == "get_weather":
        city = tool_input.get("city", "Unknown")
        print(f"  📡 Fetching weather for {city}...")
        result = await fetch_weather_forecast(city)
        print(f"  ✓ Weather data: {len(result)} days")
        return result
        
    elif tool_name == "get_images":
        city = tool_input.get("city", "Unknown")
        print(f"  📡 Fetching images for {city}...")
        result = await fetch_city_images(city)
        print(f"  ✓ Images: {len(result)} URLs")
        return result
        
    elif tool_name == "web_search":
        query = tool_input.get("query", "Unknown")
        print(f"  📡 Searching web for: {query}...")
        # Mock search result
        await asyncio.sleep(0.2)
        result = f"Search results for '{query}': Found information about {query}."
        print(f"  ✓ Search complete")
        return result
        
    else:
        raise ValueError(f"Unknown tool: {tool_name}")


def get_tools_for_binding() -> List[Dict[str, Any]]:
    """
    Get tool schemas for LLM binding.
    Used by node_call_llm_with_tools to bind tools to the LLM.
    
    Returns:
        List of tool schema dictionaries
    """
    return TOOL_SCHEMAS