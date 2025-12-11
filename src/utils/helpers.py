"""
Helper utilities for the Travel Assistant.

Provides utility functions for data processing and formatting.

Usage:
    from src.utils.helpers import format_city_name, validate_city
"""

from typing import Optional, Dict, List
from datetime import datetime
import re


def format_city_name(city: str) -> str:
    """
    Format city name to standard format.
    
    Examples:
        "PARIS" -> "Paris"
        "new york" -> "New York"
        "los-angeles" -> "Los Angeles"
    
    Args:
        city: Raw city name
        
    Returns:
        Formatted city name
    """
    if not city:
        return ""
    
    # Replace hyphens with spaces
    city = city.replace("-", " ")
    
    # Title case each word
    city = " ".join(word.capitalize() for word in city.split())
    
    return city.strip()


def validate_city(city: str, max_length: int = 100) -> bool:
    """
    Validate city name.
    
    Args:
        city: City name to validate
        max_length: Maximum allowed length
        
    Returns:
        True if valid, False otherwise
    """
    if not city:
        return False
    
    if len(city) > max_length:
        return False
    
    # Check for valid characters (letters, spaces, hyphens)
    if not re.match(r"^[a-zA-Z\s\-]+$", city):
        return False
    
    return True


def truncate_text(text: str, max_length: int = 500, suffix: str = "...") -> str:
    """
    Truncate text to max length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    # Truncate and add suffix
    return text[:max_length - len(suffix)] + suffix


def format_temperature(celsius: float) -> str:
    """
    Format temperature value.
    
    Args:
        celsius: Temperature in Celsius
        
    Returns:
        Formatted temperature string
    """
    if celsius is None:
        return "N/A"
    
    return f"{celsius:.1f}°C"


def format_date(date_str: str) -> str:
    """
    Format date string.
    
    Args:
        date_str: Date string (YYYY-MM-DD format)
        
    Returns:
        Formatted date string
    """
    if not date_str:
        return "N/A"
    
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%a, %b %d")
    except (ValueError, TypeError):
        return date_str


def parse_cache_status(cache_hit: bool) -> Dict[str, str]:
    """
    Parse cache hit status to display info.
    
    Args:
        cache_hit: Whether it was a cache hit
        
    Returns:
        Dictionary with status info
    """
    if cache_hit:
        return {
            "status": "Cache Hit",
            "icon": "✅",
            "description": "Used pre-loaded data (fast)",
            "color": "success"
        }
    else:
        return {
            "status": "Cache Miss",
            "icon": "🔍",
            "description": "Searched the web (slower)",
            "color": "info"
        }


def extract_city_from_query(query: str) -> Optional[str]:
    """
    Extract city name from user query.
    
    Examples:
        "Tell me about Paris" -> "Paris"
        "What's the weather in Tokyo?" -> "Tokyo"
        "I want to visit New York" -> "New York"
    
    Args:
        query: User query
        
    Returns:
        Extracted city name, or None
    """
    if not query:
        return None
    
    # Common prefixes to remove
    prefixes = [
        "tell me about",
        "what.*about",
        "weather in",
        "visit",
        "go to",
        "travel to",
        "information about",
        "facts about"
    ]
    
    text = query.lower().strip()
    
    # Remove prefixes
    for prefix in prefixes:
        import re
        text = re.sub(f"^{prefix}\\s*", "", text)
    
    # Remove common suffixes
    suffixes = ["please", "?", ".", "!"]
    for suffix in suffixes:
        text = text.replace(suffix, "")
    
    # Get first capitalized phrase (likely city name)
    words = text.split()
    city = " ".join(words).strip()
    
    if city:
        return format_city_name(city)
    
    return None


def get_weather_emoji(condition: str) -> str:
    """
    Get emoji for weather condition.
    
    Args:
        condition: Weather condition string
        
    Returns:
        Appropriate emoji
    """
    condition = condition.lower()
    
    emoji_map = {
        "sunny": "☀️",
        "clear": "🌤️",
        "cloudy": "☁️",
        "rainy": "🌧️",
        "rain": "🌧️",
        "snowy": "❄️",
        "snow": "❄️",
        "windy": "💨",
        "foggy": "🌫️",
        "humid": "💧"
    }
    
    for key, emoji in emoji_map.items():
        if key in condition:
            return emoji
    
    return "🌡️"


def create_weather_summary(weather_data: List) -> str:
    """
    Create text summary of weather data.
    
    Args:
        weather_data: List of WeatherDataPoint objects
        
    Returns:
        Text summary
    """
    if not weather_data:
        return "No weather data available"
    
    summaries = []
    for point in weather_data[:3]:  # First 3 days
        emoji = get_weather_emoji(point.condition)
        summary = f"{emoji} {format_date(point.date)}: {format_temperature(point.temperature)}, {point.condition}"
        summaries.append(summary)
    
    return "\n".join(summaries)


def batch_list(items: List, batch_size: int = 3) -> List[List]:
    """
    Batch a list into chunks.
    
    Args:
        items: List to batch
        batch_size: Size of each batch
        
    Returns:
        List of batches
    """
    batches = []
    for i in range(0, len(items), batch_size):
        batches.append(items[i:i + batch_size])
    return batches