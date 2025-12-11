"""
Utils module for the Travel Assistant.

Provides logging, formatting, and helper utilities.

Components:
- logger.py: Structured logging setup
- helpers.py: Data processing and formatting utilities

Usage:
    from src.utils.logger import get_logger
    from src.utils.helpers import format_city_name, validate_city
"""

from src.utils.logger import (
    setup_logging,
    get_logger,
    LogContext
)

from src.utils.helpers import (
    format_city_name,
    validate_city,
    truncate_text,
    format_temperature,
    format_date,
    parse_cache_status,
    extract_city_from_query,
    get_weather_emoji,
    create_weather_summary,
    batch_list
)


__all__ = [
    # Logger
    "setup_logging",
    "get_logger",
    "LogContext",
    # Helpers
    "format_city_name",
    "validate_city",
    "truncate_text",
    "format_temperature",
    "format_date",
    "parse_cache_status",
    "extract_city_from_query",
    "get_weather_emoji",
    "create_weather_summary",
    "batch_list",
]