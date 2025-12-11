"""
Mock Image Search API for the Travel Assistant.

This module simulates an image search API (like Unsplash) with:
- Realistic latency (0.3s)
- Reliable Wikimedia Commons URLs (Stable, Allow Hotlinking)
- Multiple images per city
- Fallback for unknown cities

Usage:
    from src.mock_apis.image_mock import fetch_city_images
    
    images = await fetch_city_images("Paris")
    # Returns: List[str] of image URLs
"""

import asyncio


async def fetch_city_images(city: str) -> list:
    """
    Fetch high-quality images for a city.
    
    Simulates image search API with:
    - Network latency (0.3s)
    - Real, working image URLs from Wikimedia Commons
    - Multiple images per city
    - Fallback placeholder for unknown cities
    
    Args:
        city: City name (e.g., "Paris", "Tokyo", "New York")
        
    Returns:
        List of image URLs (strings)
    """
    # Simulate network latency
    await asyncio.sleep(0.3)
    
    # Pre-loaded image URLs for known cities
    # Using Wikimedia Commons URLs because they are stable and allow hotlinking.
    image_database = {
        "Paris": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques_-_Paris_-_20140824.jpg/640px-La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques_-_Paris_-_20140824.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Louvre_Museum_Wikimedia_Commons.jpg/640px-Louvre_Museum_Wikimedia_Commons.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Paris_Night.jpg/640px-Paris_Night.jpg"
        ],
        "Tokyo": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Skyscrapers_of_Shinjuku_2009_January.jpg/640px-Skyscrapers_of_Shinjuku_2009_January.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Tokyo_from_the_top_of_the_SkyTree.JPG/440px-Tokyo_from_the_top_of_the_SkyTree.JPG",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Tokyo_station_from_marunouchi_oazo.JPG/640px-Tokyo_station_from_marunouchi_oazo.JPG"
        ],
        "New York": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/View_of_Empire_State_Building_from_Rockefeller_Center_New_York_City_dllu.jpg/640px-View_of_Empire_State_Building_from_Rockefeller_Center_New_York_City_dllu.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Empire_State_Building_from_the_Top_of_the_Rock.jpg/640px-Empire_State_Building_from_the_Top_of_the_Rock.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Above_Gotham.jpg/640px-Above_Gotham.jpg"
        ],
        "London": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/London_Skyline_%28125508655%29.jpeg/640px-London_Skyline_%28125508655%29.jpeg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Palace_of_Westminster_from_the_dome_on_Methodist_Central_Hall.jpg/640px-Palace_of_Westminster_from_the_dome_on_Methodist_Central_Hall.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Palace_of_Westminster_from_the_dome_on_Methodist_Central_Hall_%28cropped%29.jpg/640px-Palace_of_Westminster_from_the_dome_on_Methodist_Central_Hall_%28cropped%29.jpg"
        ],
        "Sydney": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Sydney_Opera_House_and_Harbour_Bridge_Dusk_%282%29_2019.jpg/640px-Sydney_Opera_House_and_Harbour_Bridge_Dusk_%282%29_2019.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Sydney_Opera_House_-_Dec_2008.jpg/640px-Sydney_Opera_House_-_Dec_2008.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Bondi_Beach_2006.jpg/640px-Bondi_Beach_2006.jpg"
        ],
        "Barcelona": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Sagrada_Familia_2022.jpg/640px-Sagrada_Familia_2022.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Barcelona_beach.jpg/640px-Barcelona_beach.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Park_Guell_Barcelona.jpg/640px-Park_Guell_Barcelona.jpg"
        ],
        "Dubai": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Dubai_Skylines_at_night_%28Pexels_3787839%29.jpg/640px-Dubai_Skylines_at_night_%28Pexels_3787839%29.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Burj_Khalifa.jpg/460px-Burj_Khalifa.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Dubai_Marina_Skyline.jpg/640px-Dubai_Marina_Skyline.jpg"
        ]
    }
    
    # Normalize input for case-insensitive lookup
    city_key = None
    for key in image_database:
        if key.lower() == city.lower():
            city_key = key
            break
            
    # Return images for known city
    if city_key:
        print(f"✅ Image API: Found {len(image_database[city_key])} images for {city_key}")
        return image_database[city_key]
    else:
        print(f"⚠️  Image API: No images for {city}, returning placeholder")
        # Return placeholder for unknown cities
        # Using Wikimedia generic placeholders where possible or reliable placeholders
        return [
            f"https://placehold.co/600x400?text={city}+Image+1",
            f"https://placehold.co/600x400?text={city}+Image+2",
            f"https://placehold.co/600x400?text={city}+Image+3",
        ]


async def search_city_images(query: str, num_results: int = 3) -> list:
    """
    Search for images related to a query (simplified).
    """
    # Simulate latency
    await asyncio.sleep(0.2)
    
    # Use generic nature images from Wikimedia for fallback search
    return [
        "https://upload.wikimedia.org/wikipedia/commons/9/94/Mumbai_Downtown.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Colosseum_in_Rome%2C_Italy_-_April_2007.jpg/640px-Colosseum_in_Rome%2C_Italy_-_April_2007.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Milky_Way_Arch_over_Yosemite_Valley.jpg/640px-Milky_Way_Arch_over_Yosemite_Valley.jpg"
    ][:num_results]


async def get_landmark_images(city: str) -> list:
    """
    Get famous landmark images for a city.
    """
    return await fetch_city_images(city)