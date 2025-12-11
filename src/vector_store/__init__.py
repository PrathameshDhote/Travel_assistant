"""
Vector store module for the Travel Assistant.

This module handles ChromaDB initialization and city data management.

Components:
- setup.py: ChromaDB client initialization and population
- city_data.py: Pre-loaded city facts and metadata

Usage:
    from src.vector_store.setup import populate_vector_store
    
    client, collection = populate_vector_store()
    # Use in graph module for cache hit detection
"""

from src.vector_store.setup import (
    populate_vector_store,
    query_vector_store,
    get_city_fact,
    reset_vector_store,
    get_or_create_vector_store
)

from src.vector_store.city_data import (
    CITY_FACTS,
    CITY_METADATA,
    get_city_fact as get_city_fact_data,
    get_city_attractions,
    get_city_metadata,
    get_all_cities,
    is_city_in_store
)


__all__ = [
    # Setup functions
    "populate_vector_store",
    "query_vector_store",
    "get_city_fact",
    "reset_vector_store",
    "get_or_create_vector_store",
    # City data
    "CITY_FACTS",
    "CITY_METADATA",
    "get_city_fact_data",
    "get_city_attractions",
    "get_city_metadata",
    "get_all_cities",
    "is_city_in_store",
]