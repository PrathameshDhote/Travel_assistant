"""
Mock APIs module for the Travel Assistant.

This module provides simulated APIs that mimic real-world services:
- Weather API (fetch_weather_forecast)
- Image Search API (fetch_city_images)
- Web Search API (web_search)

All APIs include:
- Realistic network latency
- Pre-loaded data for 5+ cities
- Fallback/placeholder data for unknown queries
- Type safety with clear return types

Usage:
    from src.mock_apis.weather_mock import fetch_weather_forecast
    from src.mock_apis.image_mock import fetch_city_images
    from src.mock_apis.search_mock import web_search
    
    weather = await fetch_weather_forecast("Paris")
    images = await fetch_city_images("Paris")
    results = await web_search("Tell me about Paris")

Pre-loaded Cities:
    - Paris
    - Tokyo
    - New York
    - London
    - Sydney
    - Barcelona (images only)
    - Dubai (images only)

Unknown Cities:
    - Weather: Generated mock data with reasonable ranges
    - Images: Placeholder URLs
    - Search: Generic response with fallback text
"""

from src.mock_apis.weather_mock import (
    fetch_weather_forecast,
    get_current_weather
)

from src.mock_apis.image_mock import (
    fetch_city_images,
    search_city_images,
    get_landmark_images
)

from src.mock_apis.search_mock import (
    web_search,
    search_city_info,
    get_travel_tips
)


__all__ = [
    # Weather functions
    "fetch_weather_forecast",
    "get_current_weather",
    # Image functions
    "fetch_city_images",
    "search_city_images",
    "get_landmark_images",
    # Search functions
    "web_search",
    "search_city_info",
    "get_travel_tips",
]