"""
Mock Web Search API for the Travel Assistant.

This module simulates a web search API (like Tavily or DuckDuckGo) with:
- Realistic latency (0.4s)
- Relevant search results for cities
- Structured result format
- Fallback for unknown queries

Usage:
    from src.mock_apis.search_mock import web_search
    
    results = await web_search("Tell me about Paris")
    # Returns: str with search results
"""

import asyncio


async def web_search(query: str) -> str:
    """
    Mock web search for city information.
    
    Simulates a search engine with:
    - Network latency (0.4s)
    - Relevant results for city queries
    - Natural language responses
    - Fallback for unknown cities
    
    Args:
        query: Search query about a city
        
    Returns:
        String with search results summary
    """
    # Simulate network latency
    await asyncio.sleep(0.4)
    
    # Extract city name from query (simple extraction)
    query_lower = query.lower()
    
    # Pre-loaded search results for known cities
    search_results = {
        "paris": """
        Paris, the capital of France, is one of the most iconic cities in the world. 
        Known for the Eiffel Tower, world-class museums like the Louvre, charming cafés, 
        and romantic Seine River cruises. Paris is the 4th most visited city globally 
        with around 30 million visitors annually. The city is renowned for its architecture, 
        art, fashion, and gastronomy. Key attractions include Notre-Dame Cathedral, 
        Arc de Triomphe, and Sacré-Cœur.
        """,
        
        "tokyo": """
        Tokyo, Japan's capital, is a vibrant metropolis seamlessly blending ancient temples 
        with cutting-edge technology. Famous for sushi, anime culture, efficient transportation, 
        and the iconic Shibuya Crossing. With over 37 million residents, Tokyo is the world's 
        most populous metropolitan area. The city offers everything from traditional tea ceremonies 
        to neon-lit gaming districts. Key areas include Shibuya, Shinjuku, Asakusa, and Akihabara.
        """,
        
        "new york": """
        New York City, the city that never sleeps, is a global center of finance, art, 
        and entertainment. Home to Broadway, Central Park, the Statue of Liberty, and 
        iconic skyscrapers like the Empire State Building. NYC attracts over 60 million 
        visitors annually. The city is known for its diversity, world-renowned museums, 
        fine dining, and vibrant neighborhoods including Manhattan, Brooklyn, Queens, 
        the Bronx, and Staten Island.
        """,
        
        "london": """
        London, the capital of the United Kingdom, is a historic city blending medieval 
        architecture with modern innovation. Home to Big Ben, Tower of London, Buckingham Palace, 
        and the British Museum. London attracts over 18 million international visitors annually. 
        The city is a major global financial and cultural hub with diverse neighborhoods 
        like Westminster, South Bank, and Camden.
        """,
        
        "sydney": """
        Sydney, Australia's largest city, is famous for the Sydney Opera House and Harbour Bridge. 
        Known for stunning beaches like Bondi and Coogee, laid-back beach culture, and outdoor activities. 
        The city offers diverse dining, world-class museums, and beautiful coastal scenery. 
        Sydney is a major hub for technology and creative industries with a population of over 5 million.
        """,
        
        "barcelona": """
        Barcelona, Catalonia's capital, is renowned for its unique architecture, especially 
        the works of Antoni Gaudí like the Sagrada Familia. The city blends Gothic quarters, 
        beaches, and vibrant neighborhoods like La Rambla. Barcelona is famous for FC Barcelona 
        football club, tapas culture, and Mediterranean charm. Over 30 million visitors 
        explore the city's art, food, and architecture annually.
        """,
    }
    
    # Search for matching city in results
    for city, result in search_results.items():
        if city in query_lower:
            print(f"✅ Web Search: Found results for '{city}'")
            return result.strip()
    
    # Fallback for unknown city
    print(f"⚠️  Web Search: No data for query '{query}', returning generic response")
    return f"""
    Search results for: {query}
    
    This is a beautiful and interesting destination with rich history, culture, and attractions. 
    The city offers diverse dining, accommodations, and entertainment options for visitors. 
    Consider visiting popular landmarks, museums, parks, and local neighborhoods to experience 
    the authentic charm of this location.
    """.strip()


async def search_city_info(city: str, topic: str = "general") -> str:
    """
    Search for specific information about a city.
    
    Args:
        city: City name
        topic: Topic to search (e.g., "attractions", "food", "weather")
        
    Returns:
        String with relevant information
    """
    await asyncio.sleep(0.3)
    
    city_info = {
        "Paris": {
            "attractions": "Eiffel Tower, Louvre Museum, Notre-Dame, Sacré-Cœur",
            "food": "French cuisine, Croissants, Cheese, Wine",
            "weather": "Temperate, mild winters, cool summers",
            "general": "Capital of France, known for art, culture, and romance"
        },
        "Tokyo": {
            "attractions": "Tokyo Tower, Shibuya Crossing, Asakusa Temple",
            "food": "Sushi, Ramen, Tempura, Japanese cuisine",
            "weather": "Humid subtropical, hot summers, mild winters",
            "general": "Capital of Japan, known for technology and tradition"
        },
        "New York": {
            "attractions": "Statue of Liberty, Central Park, Empire State Building",
            "food": "Pizza, Hot dogs, Bagels, American cuisine",
            "weather": "Humid continental, cold winters, warm summers",
            "general": "Major global city, known as the city that never sleeps"
        },
    }
    
    if city in city_info and topic in city_info[city]:
        return city_info[city][topic]
    else:
        return f"Information about {city} - {topic}: Details not available"


async def get_travel_tips(city: str) -> str:
    """
    Get travel tips for a city.
    
    Args:
        city: City name
        
    Returns:
        String with travel tips
    """
    await asyncio.sleep(0.25)
    
    tips = {
        "Paris": """
        Travel Tips for Paris:
        - Best time to visit: Spring (April-May) or Fall (September-October)
        - Transportation: Use metro system, buses, or rent a bicycle
        - Language: Learn basic French phrases, many locals appreciate the effort
        - Dining: Try local bistros and cafés for authentic experience
        - Attractions: Book tickets in advance for major museums
        - Budget: Paris can be expensive; look for free attractions
        """,
        
        "Tokyo": """
        Travel Tips for Tokyo:
        - Best time to visit: Spring (March-May) or Fall (September-November)
        - Transportation: Comprehensive and efficient public transport system
        - Language: Learn basic Japanese, though English signs are common
        - Dining: Enjoy street food and local restaurants for authentic flavors
        - Etiquette: Remove shoes when entering homes and some restaurants
        - Budget: Mix of expensive and budget-friendly options available
        """,
        
        "New York": """
        Travel Tips for New York:
        - Best time to visit: Fall (September-November) or Spring (April-May)
        - Transportation: Extensive subway system, affordable and convenient
        - Neighborhoods: Explore diverse areas like Greenwich Village, Brooklyn
        - Dining: Incredible variety from street food to fine dining
        - Theater: Book Broadway shows in advance
        - Budget: Can range from budget to luxury; plan accordingly
        """,
    }
    
    return tips.get(city, f"Travel tips for {city} not available in database")