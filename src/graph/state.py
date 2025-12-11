"""
State definition for the Travel Assistant agent.

This module defines the Pydantic models and LangGraph state schema
that govern the agent's memory and data flow across nodes.
"""

from typing import List, Optional
from pydantic import BaseModel
from langchain_core.messages import BaseMessage


class WeatherDataPoint(BaseModel):
    """Structured weather forecast data point."""
    date: str
    temperature: float
    condition: str
    humidity: float

    def dict(self, **kwargs):
        """Override dict for JSON serialization."""
        return {
            "date": self.date,
            "temperature": self.temperature,
            "condition": self.condition,
            "humidity": self.humidity
        }


class StructuredOutput(BaseModel):
    """Final structured output rendered by Streamlit."""
    city_summary: str
    weather_forecast: List[WeatherDataPoint]
    image_urls: List[str]

    def dict(self, **kwargs):
        """Override dict for JSON serialization."""
        return {
            "city_summary": self.city_summary,
            "weather_forecast": [d.dict() for d in self.weather_forecast],
            "image_urls": self.image_urls
        }


class AgentState(BaseModel):
    """
    State schema for LangGraph.
    
    Tracks:
    - messages: Conversation history (HumanMessage, AIMessage, ToolMessage)
    - city_name: Extracted city from user query
    - vector_store_match: Whether city is in ChromaDB
    - cache_hit: Whether we're using cached context
    - city_summary: Pre-loaded facts from vector store (if hit)
    - weather_data: Fetched weather forecast
    - image_urls: Fetched image URLs
    - final_output: Structured response for UI
    - error_message: Any error encountered
    """
    messages: List[BaseMessage]
    city_name: Optional[str] = None
    vector_store_match: Optional[bool] = None
    cache_hit: Optional[bool] = None
    city_summary: Optional[str] = None
    weather_data: Optional[List[WeatherDataPoint]] = None
    image_urls: Optional[List[str]] = None
    final_output: Optional[StructuredOutput] = None
    error_message: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True 