"""
UI module for the Travel Assistant.

Provides Streamlit web interface for the agentic system.

Components:
- app.py: Main Streamlit application

Usage:
    streamlit run src/ui/app.py
"""

from src.ui.app import (
    initialize_session_state,
    get_graph_and_collection,
    display_weather,
    display_images,
    display_result,
    main
)


__all__ = [
    "initialize_session_state",
    "get_graph_and_collection",
    "display_weather",
    "display_images",
    "display_result",
    "main",
]