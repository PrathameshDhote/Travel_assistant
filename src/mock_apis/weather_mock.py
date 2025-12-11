
"""
Mock Weather API for the Travel Assistant.

This module simulates a real weather API with:
- Realistic latency (0.3s)
- Real date formatting
- Structured forecast data for multiple cities
- Fallback for unknown cities

Usage:
    from src.mock_apis.weather_mock import fetch_weather_forecast
    
    forecast = await fetch_weather_forecast("Paris")
    # Returns: List[WeatherDataPoint]
"""

import asyncio
from datetime import datetime, timedelta
from src.graph.state import WeatherDataPoint


async def fetch_weather_forecast(city: str) -> list:
    """
    Fetch 5-7 day weather forecast for a city.
    
    Simulates real API with:
    - Network latency (0.3s)
    - Real dates starting from tomorrow
    - Realistic temperature ranges by city
    - Humidity and weather conditions
    
    Args:
        city: City name (e.g., "Paris", "Tokyo", "New York")
        
    Returns:
        List of WeatherDataPoint objects with forecast data
    """
    # Simulate network latency
    await asyncio.sleep(0.3)
    
    # Generate dates starting from tomorrow
    base_date = datetime.now()
    dates = [
        (base_date + timedelta(days=i)).strftime("%Y-%m-%d") 
        for i in range(1, 8)
    ]
    
    # Pre-loaded weather data for known cities
    forecasts = {
        "Paris": [
            WeatherDataPoint(date=dates[0], temperature=8.5, condition="Cloudy", humidity=72),
            WeatherDataPoint(date=dates[1], temperature=7.2, condition="Rainy", humidity=85),
            WeatherDataPoint(date=dates[2], temperature=9.1, condition="Partly Cloudy", humidity=68),
            WeatherDataPoint(date=dates[3], temperature=6.8, condition="Clear", humidity=55),
            WeatherDataPoint(date=dates[4], temperature=5.5, condition="Cold", humidity=48),
            WeatherDataPoint(date=dates[5], temperature=6.3, condition="Overcast", humidity=62),
            WeatherDataPoint(date=dates[6], temperature=7.8, condition="Cloudy", humidity=70),
        ],
        "Tokyo": [
            WeatherDataPoint(date=dates[0], temperature=15.3, condition="Clear", humidity=45),
            WeatherDataPoint(date=dates[1], temperature=14.8, condition="Sunny", humidity=42),
            WeatherDataPoint(date=dates[2], temperature=16.2, condition="Clear", humidity=48),
            WeatherDataPoint(date=dates[3], temperature=17.1, condition="Sunny", humidity=50),
            WeatherDataPoint(date=dates[4], temperature=15.9, condition="Partly Cloudy", humidity=55),
            WeatherDataPoint(date=dates[5], temperature=14.5, condition="Rainy", humidity=68),
            WeatherDataPoint(date=dates[6], temperature=13.2, condition="Windy", humidity=60),
        ],
        "New York": [
            WeatherDataPoint(date=dates[0], temperature=2.1, condition="Snowy", humidity=80),
            WeatherDataPoint(date=dates[1], temperature=0.5, condition="Freezing", humidity=75),
            WeatherDataPoint(date=dates[2], temperature=1.3, condition="Snow", humidity=82),
            WeatherDataPoint(date=dates[3], temperature=3.2, condition="Clear", humidity=60),
            WeatherDataPoint(date=dates[4], temperature=4.5, condition="Partly Cloudy", humidity=65),
            WeatherDataPoint(date=dates[5], temperature=2.8, condition="Cloudy", humidity=70),
            WeatherDataPoint(date=dates[6], temperature=1.9, condition="Cold", humidity=75),
        ],
        "London": [
            WeatherDataPoint(date=dates[0], temperature=9.2, condition="Rainy", humidity=78),
            WeatherDataPoint(date=dates[1], temperature=8.5, condition="Cloudy", humidity=75),
            WeatherDataPoint(date=dates[2], temperature=10.1, condition="Partly Cloudy", humidity=70),
            WeatherDataPoint(date=dates[3], temperature=9.8, condition="Overcast", humidity=72),
            WeatherDataPoint(date=dates[4], temperature=8.3, condition="Rainy", humidity=80),
            WeatherDataPoint(date=dates[5], temperature=7.9, condition="Drizzle", humidity=76),
            WeatherDataPoint(date=dates[6], temperature=9.5, condition="Cloudy", humidity=74),
        ],
        "Sydney": [
            WeatherDataPoint(date=dates[0], temperature=26.5, condition="Sunny", humidity=45),
            WeatherDataPoint(date=dates[1], temperature=27.2, condition="Clear", humidity=42),
            WeatherDataPoint(date=dates[2], temperature=25.8, condition="Partly Cloudy", humidity=48),
            WeatherDataPoint(date=dates[3], temperature=24.3, condition="Cloudy", humidity=55),
            WeatherDataPoint(date=dates[4], temperature=22.9, condition="Rainy", humidity=68),
            WeatherDataPoint(date=dates[5], temperature=23.5, condition="Showers", humidity=72),
            WeatherDataPoint(date=dates[6], temperature=25.1, condition="Clear", humidity=50),
        ],
    }
    
    # Return forecast for known city, or generate random for unknown
    if city in forecasts:
        print(f"✅ Weather API: Found data for {city}")
        return forecasts[city]
    else:
        print(f"⚠️  Weather API: No data for {city}, generating mock data")
        # Generate fallback data with reasonable temperatures
        return [
            WeatherDataPoint(
                date=dates[i],
                temperature=15 + (i % 3),
                condition=["Sunny", "Cloudy", "Rainy"][i % 3],
                humidity=60 + (i % 2) * 10
            )
            for i in range(7)
        ]


async def get_current_weather(city: str) -> dict:
    """
    Fetch current weather for a city (simplified version).
    
    Args:
        city: City name
        
    Returns:
        Dict with current conditions
    """
    await asyncio.sleep(0.2)
    
    current_conditions = {
        "Paris": {"temp": 8.5, "condition": "Cloudy", "humidity": 72},
        "Tokyo": {"temp": 15.3, "condition": "Clear", "humidity": 45},
        "New York": {"temp": 2.1, "condition": "Snowy", "humidity": 80},
        "London": {"temp": 9.2, "condition": "Rainy", "humidity": 78},
        "Sydney": {"temp": 26.5, "condition": "Sunny", "humidity": 45},
    }
    
    if city in current_conditions:
        return current_conditions[city]
    else:
        return {"temp": 20, "condition": "Unknown", "humidity": 60}