"""
Graph module for the Travel Assistant.

This module exports all graph-related components:
- State definitions (AgentState, StructuredOutput, WeatherDataPoint)
- Node implementations (all 6 nodes)
- Tool definitions (get_weather, get_images, web_search)
- Graph builder (build_travel_graph)

Usage:
    from src.graph import AgentState, build_travel_graph
    
    # Build graph
    graph = build_travel_graph(chromadb_collection)
    
    # Invoke with initial state
    state = AgentState(messages=[HumanMessage(content="Tell me about Paris")])
    result = graph.invoke(state, config={"configurable": {"thread_id": "main"}})
"""

from src.graph.state import (
    AgentState,
    StructuredOutput,
    WeatherDataPoint
)

from src.graph.nodes import (
    node_classify_query,
    node_check_vector_store,
    node_use_cached_context,
    node_call_llm_with_tools,
    node_execute_tools_parallel,
    node_format_output
)

from src.graph.tools import (
    execute_tool,
    get_tools_for_binding,
    TOOL_SCHEMAS
)

from src.graph.graph_builder import build_travel_graph


__all__ = [
    # State
    "AgentState",
    "StructuredOutput",
    "WeatherDataPoint",
    # Nodes
    "node_classify_query",
    "node_check_vector_store",
    "node_use_cached_context",
    "node_call_llm_with_tools",
    "node_execute_tools_parallel",
    "node_format_output",
    # Tools
    "execute_tool",
    "get_tools_for_binding",
    "TOOL_SCHEMAS",
    # Builder
    "build_travel_graph"
]