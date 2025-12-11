import functools
from langgraph.graph import StateGraph, START, END
# We use MemorySaver because it supports async execution (ainvoke) natively,
# unlike SqliteSaver which is sync-only.
from langgraph.checkpoint.memory import MemorySaver

from src.graph.state import AgentState
from src.graph.nodes import (
    node_classify_query,
    node_check_vector_store,
    node_use_cached_context,
    node_call_llm_with_tools,
    node_execute_tools_parallel,
    node_format_output
)

def build_travel_graph(collection):
    """
    Build the agentic graph with conditional routing.
    
    This function demonstrates:
    - Clear graph topology with 2 distinct paths
    - Conditional edge routing based on cache hit/miss
    - Distinction 3: Checkpoint/Memory for context preservation
    
    Args:
        collection: Vector store collection (ChromaDB or FAISS)
        
    Returns:
        Compiled LangGraph ready for execution
    """
    
    # 1. Create state graph
    workflow = StateGraph(AgentState)
    
    # 2. Add Nodes
    workflow.add_node("classify_query", node_classify_query)
    
    # Node 2: Check if city is in vector store
    # We use functools.partial to pass the 'collection' argument 
    # while keeping the function signature compatible with LangGraph
    workflow.add_node(
        "check_vector_store",
        functools.partial(node_check_vector_store, collection=collection)
    )
    
    # Node 3: Use cached context (Path A - Cache Hit)
    workflow.add_node("use_cached_context", node_use_cached_context)
    
    # Node 4: Call LLM to decide tools (Path B - Cache Miss)
    workflow.add_node("call_llm", node_call_llm_with_tools)
    
    # Node 5: Execute tools in parallel (Distinction 1 + 2)
    workflow.add_node("execute_tools", node_execute_tools_parallel)
    
    # Node 6: Format output as structured JSON
    workflow.add_node("format_output", node_format_output)
    
    # 3. Define Standard Edges
    workflow.add_edge(START, "classify_query")
    workflow.add_edge("classify_query", "check_vector_store")
    
    # 4. Define Conditional Routing Logic
    def route_based_on_cache(state: AgentState) -> str:
        """
        Decision function: Should we use cached context or fetch from web?
        
        Returns:
            "cache_hit" if city found in vector store (Path A)
            "cache_miss" if city not found (Path B)
        """
        # Safely access the state dictionary
        is_cache_hit = state.vector_store_match
        
        if is_cache_hit:
            print(f"🔀 Routing decision: CACHE HIT → Use cached context path")
            return "cache_hit"
        else:
            print(f"🔀 Routing decision: CACHE MISS → Use LLM + tools path")
            return "cache_miss"
    
    # Add the conditional edge (The "Switch")
    workflow.add_conditional_edges(
        "check_vector_store",
        route_based_on_cache,
        {
            "cache_hit": "use_cached_context",   # Path A: Fast cached path
            "cache_miss": "call_llm"             # Path B: Search + tools path
        }
    )
  
    # Path A Flow
    workflow.add_edge("use_cached_context", "format_output")
    
    # Path B Flow
    workflow.add_edge("call_llm", "execute_tools")
    workflow.add_edge("execute_tools", "format_output")
    
    # Final Edge
    workflow.add_edge("format_output", END)
    
    # 5. Setup Memory (Checkpointer)
    # FIX: Replaced SqliteSaver with MemorySaver.
    # MemorySaver is thread-safe and works with async graphs (ainvoke),
    # fixing the "SqliteSaver does not support async methods" error.
    memory = MemorySaver()
    
    # Compile the graph with checkpointer
    graph = workflow.compile(checkpointer=memory)
    
    print("✅ Graph built with:")
    print("   - 6 nodes (classify, cache check, cached path, LLM, tools, format)")
    print("   - Conditional routing (cache hit vs cache miss)")
    print("   - Async-compatible MemorySaver for context preservation")
    
    return graph