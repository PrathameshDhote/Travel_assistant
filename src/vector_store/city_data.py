"""
City data for vector store.

This module contains pre-loaded facts about cities that will be embedded
and stored in ChromaDB for the cache hit path of the agentic system.

These facts are detailed enough to provide meaningful context to users
without requiring a web search.
"""

# City facts with detailed information
CITY_FACTS = {
    "Paris": {
        "summary": """
        Paris, the capital of France, is one of the most iconic and enchanting cities in the world.
        Known worldwide for the majestic Eiffel Tower, world-class museums like the Louvre, charming 
        cafés, and romantic Seine River cruises. Paris is the 4th most visited city globally with 
        around 30 million visitors annually.
        """,
        "attractions": [
            "Eiffel Tower",
            "Louvre Museum",
            "Notre-Dame Cathedral",
            "Arc de Triomphe",
            "Sacré-Cœur Basilica",
            "Palace of Versailles",
            "Champs-Élysées",
            "Musée d'Orsay"
        ],
        "cuisine": "French haute cuisine, croissants, cheese, wine",
        "best_time": "April-May (Spring) or September-October (Fall)",
        "language": "French",
        "currency": "Euro (EUR)",
        "population": "2.2 million (city), 12 million (metro area)",
        "founded": "3rd century BC"
    },
    
    "Tokyo": {
        "summary": """
        Tokyo, Japan's capital, is a vibrant metropolis seamlessly blending ancient traditions 
        with cutting-edge technology. With over 37 million residents, it's the world's most 
        populous metropolitan area. Famous for sushi, anime culture, efficient transportation, 
        and the iconic Shibuya Crossing.
        """,
        "attractions": [
            "Tokyo Tower",
            "Shibuya Crossing",
            "Senso-ji Temple (Asakusa)",
            "Meiji Shrine",
            "Tokyo Skytree",
            "Akihabara",
            "Tsukiji Market",
            "Imperial Palace"
        ],
        "cuisine": "Sushi, ramen, tempura, Japanese cuisine",
        "best_time": "March-May (Spring) or September-November (Fall)",
        "language": "Japanese",
        "currency": "Japanese Yen (JPY)",
        "population": "37.4 million (metro area)",
        "founded": "1457"
    },
    
    "New York": {
        "summary": """
        New York City, the city that never sleeps, is a global center of finance, art, 
        entertainment, and culture. Home to over 8 million residents, NYC attracts over 60 
        million visitors annually. Famous for its iconic skyline, Broadway theaters, Central 
        Park, Statue of Liberty, and world-renowned museums.
        """,
        "attractions": [
            "Statue of Liberty",
            "Central Park",
            "Empire State Building",
            "Times Square",
            "One World Trade Center",
            "Brooklyn Bridge",
            "Metropolitan Museum of Art",
            "American Museum of Natural History"
        ],
        "cuisine": "Pizza, hot dogs, bagels, diverse international cuisines",
        "best_time": "April-May (Spring) or September-November (Fall)",
        "language": "English",
        "currency": "US Dollar (USD)",
        "population": "8.3 million (city), 20 million (metro area)",
        "founded": "1624"
    },
    
    "London": {
        "summary": """
        London, the capital of the United Kingdom, is a historic city blending medieval 
        architecture with modern innovation. A major global financial and cultural hub, 
        London attracts over 18 million international visitors annually. Home to Big Ben, 
        Tower of London, Buckingham Palace, and the British Museum.
        """,
        "attractions": [
            "Big Ben & Houses of Parliament",
            "Tower of London",
            "Buckingham Palace",
            "Tower Bridge",
            "British Museum",
            "Westminster Abbey",
            "St. Paul's Cathedral",
            "Trafalgar Square"
        ],
        "cuisine": "Fish and chips, Sunday roast, afternoon tea, Indian food",
        "best_time": "May-September (Summer)",
        "language": "English",
        "currency": "British Pound (GBP)",
        "population": "9 million (city), 14 million (metro area)",
        "founded": "43 AD"
    },
    
    "Sydney": {
        "summary": """
        Sydney, Australia's largest city, is famous for the iconic Sydney Opera House 
        and Harbour Bridge. Known for stunning beaches like Bondi and Coogee, laid-back 
        beach culture, and outdoor activities. A major hub for technology and creative 
        industries with over 5 million residents.
        """,
        "attractions": [
            "Sydney Opera House",
            "Sydney Harbour Bridge",
            "Bondi Beach",
            "Taronga Zoo",
            "Royal Botanic Garden",
            "Coogee Beach",
            "Manly Beach",
            "Blue Mountains"
        ],
        "cuisine": "Seafood, meat pies, lamingtons, coffee culture",
        "best_time": "September-November (Spring) or December-February (Summer)",
        "language": "English",
        "currency": "Australian Dollar (AUD)",
        "population": "5.2 million",
        "founded": "1788"
    }
}


# Additional metadata for each city
CITY_METADATA = {
    "Paris": {
        "continent": "Europe",
        "region": "Northern France",
        "timezone": "CET",
        "climate": "Oceanic",
        "famous_for": ["Art", "Romance", "Architecture", "Cuisine"],
        "must_see": ["Eiffel Tower", "Louvre", "Notre-Dame"],
    },
    "Tokyo": {
        "continent": "Asia",
        "region": "Eastern Japan",
        "timezone": "JST",
        "climate": "Humid subtropical",
        "famous_for": ["Technology", "Anime", "Temples", "Food"],
        "must_see": ["Shibuya Crossing", "Senso-ji Temple", "Tokyo Tower"],
    },
    "New York": {
        "continent": "North America",
        "region": "Northeastern USA",
        "timezone": "EST",
        "climate": "Humid continental",
        "famous_for": ["Business", "Arts", "Diversity", "Entertainment"],
        "must_see": ["Statue of Liberty", "Central Park", "Times Square"],
    },
    "London": {
        "continent": "Europe",
        "region": "Southern England",
        "timezone": "GMT/BST",
        "climate": "Temperate oceanic",
        "famous_for": ["History", "Culture", "Royalty", "Commerce"],
        "must_see": ["Big Ben", "Tower of London", "Tower Bridge"],
    },
    "Sydney": {
        "continent": "Oceania",
        "region": "Eastern Australia",
        "timezone": "AEDT/AEST",
        "climate": "Subtropical",
        "famous_for": ["Beaches", "Opera House", "Outdoor Activities", "Lifestyle"],
        "must_see": ["Opera House", "Harbour Bridge", "Bondi Beach"],
    }
}


def get_city_fact(city: str) -> str:
    """Get the summary fact for a city."""
    if city in CITY_FACTS:
        return CITY_FACTS[city]["summary"].strip()
    return ""


def get_city_attractions(city: str) -> list:
    """Get attractions for a city."""
    if city in CITY_FACTS:
        return CITY_FACTS[city].get("attractions", [])
    return []


def get_city_metadata(city: str) -> dict:
    """Get metadata for a city."""
    if city in CITY_METADATA:
        return CITY_METADATA[city]
    return {}


def get_all_cities() -> list:
    """Get list of all pre-loaded cities."""
    return list(CITY_FACTS.keys())


def is_city_in_store(city: str) -> bool:
    """Check if a city is pre-loaded in the store."""
    return city in CITY_FACTS