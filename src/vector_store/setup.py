"""
Vector store setup for the Travel Assistant.

This module initializes ChromaDB and populates it with pre-loaded city facts
for 3 cities (Paris, Tokyo, New York).

These cities will be used for the cache hit path in the agentic graph,
demonstrating intelligent routing without requiring web search.

Usage:
    from src.vector_store.setup import populate_vector_store
    
    client, collection = populate_vector_store()
    # collection is ready to use with graph module
"""

import chromadb
from chromadb.config import Settings


def populate_vector_store():
    """
    Initialize ChromaDB and populate with pre-loaded city facts.
    """
    
    # Initialize ChromaDB client with in-memory storage.
    # We use the modern Client() initialization which works for newer versions.
    client = chromadb.Client(settings=Settings(
        allow_reset=True,
        anonymized_telemetry=False
    ))
    
    # Get or create collection
    # We explicitly set the distance metric to cosine.
    collection = client.get_or_create_collection(
        name="cities",
        metadata={"hnsw:space": "cosine"}
    )
    
    # Pre-loaded city facts (detailed summaries)
    city_facts = {
        "Paris": """
        Paris, the capital of France, is one of the most iconic and enchanting cities in the world.
        Known worldwide for the majestic Eiffel Tower, world-class museums like the Louvre, charming 
        cafés, and romantic Seine River cruises. Paris is the 4th most visited city globally with 
        around 30 million visitors annually. The city is renowned for its exceptional architecture, 
        rich art heritage, fashion industry leadership, and exquisite gastronomy. 
        
        Key attractions include Notre-Dame Cathedral, the Arc de Triomphe, Sacré-Cœur basilica, 
        and the Palace of Versailles. The city is divided into 20 arrondissements (districts), 
        each with unique character and attractions. Paris offers world-famous cuisine from Michelin-starred 
        restaurants to charming bistros. The city's romantic atmosphere, historic monuments, and 
        vibrant culture make it a must-visit destination for travelers worldwide.
        """,
        
        "Tokyo": """
        Tokyo, Japan's capital and largest city, is a vibrant metropolis that seamlessly blends 
        ancient traditions with cutting-edge technology. With over 37 million residents, Tokyo is 
        the world's most populous metropolitan area. The city is famous for sushi, anime culture, 
        efficient transportation systems, the iconic Shibuya Crossing, and ultra-modern architecture.
        
        Tokyo offers everything from traditional tea ceremonies in historic temples to neon-lit gaming 
        districts in Akihabara. Key areas include Shibuya (fashion and entertainment), Shinjuku 
        (business and nightlife), Asakusa (traditional temples), and Akihabara (technology and anime). 
        The city is known for its cleanliness, punctuality, politeness, and exceptional public transportation. 
        Tokyo's food scene is extraordinary, offering diverse cuisines from street food to 
        Michelin-starred restaurants. The city blends harmony with technology, tradition with innovation, 
        making it one of the most fascinating cities on Earth.
        """,
        
        "New York": """
        New York City, often called "The City That Never Sleeps," is a global center of finance, 
        art, entertainment, and culture. Home to over 8 million residents, NYC is the most populous 
        city in the United States. The city attracts over 60 million visitors annually, making it 
        one of the world's most visited cities. NYC is famous for its iconic skyline, Broadway theaters, 
        Central Park, Statue of Liberty, and world-renowned museums.
        
        The city's five boroughs (Manhattan, Brooklyn, Queens, The Bronx, Staten Island) offer diverse 
        neighborhoods with unique characters and attractions. Manhattan's iconic landmarks include the 
        Empire State Building, Times Square, One World Trade Center, and Wall Street. Brooklyn is known 
        for its hipster culture, brownstones, and waterfront views. NYC offers unparalleled dining, 
        shopping, entertainment, and cultural experiences. The city's energy, diversity, ambition, and 
        cultural significance make it a truly global metropolis and a must-visit destination for people worldwide.
        """
    }
    
    # Add documents to collection
    # Note: We check if data exists first to avoid duplication errors on re-runs 
    if collection.count() == 0:
        for city, fact in city_facts.items():
            collection.add(
                ids=[city.lower()],
                documents=[fact.strip()],
                metadatas=[{
                    "city": city,
                    "type": "city_facts",
                    "cached": "true"
                }]
            )
            print(f"✅ Added {city} to vector store")
    else:
        print(f"ℹ️  Vector store already contains {collection.count()} documents")
    
    return client, collection


def query_vector_store(collection, city: str, threshold: float = 0.55) -> bool: # <--- CHANGED TO 0.55
    """
    Query the vector store to check if a city exists using Distance Thresholding.
    
    Args:
        collection: ChromaDB collection object
        city: City name to search for
        threshold: Distance threshold. 
                   0.55 is the sweet spot:
                   - Accepts "Paris" (Distance ~0.43)
                   - Rejects "Mumbai" vs "Tokyo" (Distance ~0.64)
                   
    Returns:
        bool: True if city found (cache hit), False otherwise (cache miss)
    """
    try:
        # Query for the single closest match
        results = collection.query(
            query_texts=[city],
            n_results=1
        )
        
        # Check if we got results AND valid distances
        if results and results['documents'] and results['distances'] and len(results['documents'][0]) > 0:
            
            # ChromaDB returns a list of lists, get the first one
            distance = results['distances'][0][0]
            
            # Get metadata to be sure (optional but good for debugging)
            # You can check if the stored city name contains the query city name
            stored_metadata = results['metadatas'][0][0] if results['metadatas'] else {}
            stored_city_name = stored_metadata.get('city', 'Unknown')
            
            print(f"🔍 Checking '{city}' against DB match '{stored_city_name}'... Distance: {distance:.4f}")
            
            # LOGIC:
            # 1. Distance check
            if distance < threshold:
                print(f"✅ CACHE HIT for {city} (Matched within threshold {threshold})")
                return True
            else:
                print(f"❌ CACHE MISS for {city} (Distance {distance:.4f} > {threshold})")
                return False
        
        else:
            print(f"❌ Cache miss for {city} (No results found)")
            return False
            
    except Exception as e:
        print(f"⚠️  Error querying vector store: {e}")
        return False


def get_city_fact(collection, city: str) -> str:
    """
    Retrieve the pre-loaded fact for a city from the vector store.
    
    Args:
        collection: ChromaDB collection object
        city: City name
        
    Returns:
        str: City fact/summary, or empty string if not found
    """
    try:
        results = collection.query(
            query_texts=[city],
            n_results=1
        )
        
        if results and results['documents'] and len(results['documents'][0]) > 0:
            return results['documents'][0][0].strip()
        else:
            return ""
            
    except Exception as e:
        print(f"⚠️  Error retrieving city fact: {e}")
        return ""


def reset_vector_store(client):
    """
    Reset the vector store (delete all data).
    
    Useful for testing and development.
    
    Args:
        client: ChromaDB client
    """
    try:
        client.reset()
        print("✅ Vector store reset")
    except Exception as e:
        print(f"⚠️  Error resetting vector store: {e}")


# Pre-initialized module-level variables (optional)
# These can be used if you want module-level initialization
_client = None
_collection = None


def get_or_create_vector_store():
    """
    Get or create the vector store (lazy initialization).
    
    Returns:
        tuple: (client, collection)
    """
    global _client, _collection
    
    if _client is None or _collection is None:
        _client, _collection = populate_vector_store()
    
    return _client, _collection