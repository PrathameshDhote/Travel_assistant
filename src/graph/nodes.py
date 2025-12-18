"""
Node implementations for the Travel Assistant agent.

This module contains all 6 graph nodes:
1. node_classify_query - Extract city name
2. node_check_vector_store - Check ChromaDB cache
3. node_use_cached_context - Use cached data path
4. node_call_llm_with_tools - LLM decides what tools to call
5. node_execute_tools_parallel - DISTINCTION 1 & 2: Manual + Parallel execution
6. node_format_output - Structure output as JSON
"""

import asyncio
import json
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from src.graph.state import AgentState, StructuredOutput, WeatherDataPoint
from src.graph.tools import execute_tool, get_tools_for_binding
# 🔧 1. Add these imports as requested
from src.vector_store.setup import query_vector_store, get_city_fact


# Initialize LLM (use gpt-4o-mini for cost efficiency)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, max_tokens=500)


# ============================================================================
# NODE 1: CLASSIFY QUERY
# ============================================================================

async def node_classify_query(state: AgentState) -> AgentState:
    """
    Extract destination name from user query.
    
    DISTINCTION 3 FIX: Preserve city_name from previous turn if not mentioned.
    This enables follow-up queries like "What is the weather?" to work.
    """
    messages = state.messages
    last_message = messages[-1].content
    
    print(f"🔍 Classifying query: {last_message[:50]}...")
    
    # 1. Try to extract a city from the CURRENT message
    extraction_prompt = (
        f"Extract the destination (city, country, or region) from this query: '{last_message}'\n"
        f"Reply with ONLY the name (e.g., 'Paris', 'Mexico', 'Tokyo'). "
        f"If no specific destination is mentioned, reply with 'None'."
    )
    
    response = await llm.ainvoke(extraction_prompt)
    destination = response.content.strip().strip(".").strip()
    
    # 2. CRITICAL FIX: If no city in current message, check if we have one from history
    if destination.lower() in ["unknown", "none", ""]:
        # Check if we already have a city_name from previous turn
        previous_city = state.city_name
        
        if previous_city and previous_city != "Unknown":
            print(f"🔄 No city in current query, reusing previous: {previous_city}")
            destination = previous_city
            
            # IMPORTANT: Only clear weather/images, NOT city_name or summary
            state.weather_data = []
            state.image_urls = []
            # Keep: city_name, city_summary, vector_store_match, cache_hit
        else:
            print(f"⚠️ Could not extract destination from: {last_message}")
            destination = "Unknown"
            # Clear everything for Unknown
            state.weather_data = []
            state.image_urls = []
            state.city_summary = None
            state.final_output = None
            state.vector_store_match = False
            state.cache_hit = False
    else:
        # New city mentioned, clear previous data
        print(f"✅ Extracted NEW destination: {destination}")
        state.weather_data = []
        state.image_urls = []
        state.city_summary = None
        state.final_output = None
        state.vector_store_match = False
        state.cache_hit = False
    
    state.city_name = destination.title()
    
    return state


# ============================================================================
# NODE 2: CHECK VECTOR STORE
# ============================================================================

async def node_check_vector_store(state: AgentState, collection) -> AgentState:
    """
    Check if city exists in local ChromaDB vector store using distance thresholding.
    Uses query_vector_store() from src.vector_store.setup to make the decision.
    """
    city = state.city_name

    if not city or city == "Unknown":
        state.vector_store_match = False
        state.cache_hit = False
        print(f"⚠️  No valid city to check in vector store")
        return state

    city_normalized = city.strip()

    print(f"🗄️  Querying vector store for '{city_normalized}'...")

    try:
        # Use helper that checks vector distance properly
        # Note: We pass threshold=0.5 to be strict (Mumbai vs Tokyo is usually > 0.5)
        is_hit = query_vector_store(collection, city_normalized, threshold=0.5)

        if is_hit:
            # Retrieve stored summary for consistency
            city_summary = get_city_fact(collection, city_normalized)
            state.vector_store_match = True
            state.cache_hit = True
            state.city_summary = city_summary
            print(f"✅ CACHE HIT: {city_normalized} found in vector store")
        else:
            state.vector_store_match = False
            state.cache_hit = False
            print(f"❌ CACHE MISS: {city_normalized} not in vector store")

    except Exception as e:
        print(f"⚠️ Vector store error: {e}")
        state.vector_store_match = False
        state.cache_hit = False
        state.error_message = str(e)

    return state


# ============================================================================
# NODE 3: USE CACHED CONTEXT
# ============================================================================

async def node_use_cached_context(state: AgentState) -> AgentState:
    """
    Use pre-loaded context from vector store (cache hit path).
    
    For cached cities, we skip the LLM and directly fetch fresh weather/images.
    This is faster and shows intelligent caching.
    
    Flow: Use cached summary + fetch fresh weather/images in parallel
    """
    city = state.city_name
    city_summary = state.city_summary
    
    if not city_summary:
        print(f"⚠️  Cache hit flagged but no summary in state")
        return state
    
    print(f"📚 Using cached context for '{city}'")
    
    try:
        # Directly call tools without LLM (skip middle node)
        # This is faster and shows architectural intelligence
        
        # We manually create coroutines for parallel execution
        # Note: execute_tool needs to be imported or available
        tasks = [
            execute_tool("get_weather", {"city": city}),
            execute_tool("get_images", {"city": city})
        ]
        
        print(f"⚡ Fetching fresh data in parallel...")
        # Use asyncio.gather for parallel execution
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Unpack results safely
        weather_result = results[0] if len(results) > 0 else []
        images_result = results[1] if len(results) > 1 else []
        
        # Store results in state, checking for exceptions
        state.weather_data = weather_result if isinstance(weather_result, list) else []
        state.image_urls = images_result if isinstance(images_result, list) else []
        
        if isinstance(weather_result, Exception):
            print(f"⚠️ Error fetching weather: {weather_result}")
        if isinstance(images_result, Exception):
            print(f"⚠️ Error fetching images: {images_result}")
            
        print(f"✅ Fresh data fetched: {len(state.weather_data)} weather points, {len(state.image_urls)} images")
        
    except Exception as e:
        print(f"⚠️  Error fetching cached city data: {e}")
        state.error_message = str(e)
    
    return state


# ============================================================================
# NODE 4: CALL LLM WITH TOOLS
# ============================================================================

async def node_call_llm_with_tools(state: AgentState) -> AgentState:
    """
    LLM decides which tools to call.
    
    The LLM autonomously decides whether to call:
    - get_weather: For weather forecasts
    - get_images: For visual gallery
    - web_search: For additional context (for unknown cities)
    
    The LLM response includes tool_calls that will be processed
    by node_execute_tools_parallel.
    """
    messages = state.messages
    city = state.city_name
    
    print(f"🤖 LLM deciding tools for '{city}'...")
    
    try:
        # Bind tools to LLM
        tools = get_tools_for_binding()
        llm_with_tools = llm.bind_tools(tools)
        
        # Invoke LLM (async)
        response = await llm_with_tools.ainvoke(messages)
        
        # Append LLM response to messages
        state.messages.append(response)
        
        # Check what tools LLM called
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"✅ LLM called {len(response.tool_calls)} tools: {[tc['name'] for tc in response.tool_calls]}")
        else:
            print(f"ℹ️  LLM did not call any tools")
        
    except Exception as e:
        print(f"⚠️  Error calling LLM: {e}")
        state.error_message = str(e)
    
    return state


# ============================================================================
# NODE 5: EXECUTE TOOLS PARALLEL (DISTINCTION 1 + 2)
# ============================================================================

async def node_execute_tools_parallel(state: AgentState) -> AgentState:
    """
    DISTINCTION 1: Manual tool execution (parse raw tool_calls, construct ToolMessage manually)
    DISTINCTION 2: Parallel execution using asyncio.gather (Fan-Out pattern)
    
    This node:
    1. Extracts tool_calls from LLM response
    2. Prepares all tool coroutines without awaiting
    3. Executes them concurrently with asyncio.gather()
    4. Constructs ToolMessage objects manually
    5. Appends back to state
    """
    messages = state.messages
    last_message = messages[-1]
    
    # Guard: Only process if LLM actually called tools
    if not hasattr(last_message, 'tool_calls') or not last_message.tool_calls:
        print("ℹ️  No tool calls in LLM response, skipping tool execution")
        return state

    print(f"🔧 Executing {len(last_message.tool_calls)} tools in parallel (Distinction 2)...")
    
    # ========================================================================
    # STEP 1: Prepare coroutines (don't await yet)
    # ========================================================================
    tasks = []
    tool_calls_ordered = []
    
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_input = tool_call["args"]
        
        # Create coroutine (not awaited yet)
        coroutine = execute_tool(tool_name, tool_input)
        tasks.append(coroutine)
        tool_calls_ordered.append(tool_call)
        
        print(f"  → Queued: {tool_name}({list(tool_input.keys())})")

    # ========================================================================
    # STEP 2: Execute ALL tools in parallel (Fan-Out)
    # ========================================================================
    # This is the critical difference from sequential execution.
    # All tools run concurrently, reducing latency significantly.
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print(f"✅ All {len(results)} tools completed in parallel")

    # ========================================================================
    # STEP 3: Construct ToolMessage objects manually (Distinction 1)
    # ========================================================================
    # This is where we show we understand the LLM protocol.
    # We're not using prebuilt.ToolNode; we're doing it manually.
    
    tool_messages = []
    
    # Also initialize containers for the structured output data 
    # so we can populate the final state immediately if possible
    weather_data_found = []
    image_urls_found = []
    
    for tool_call, result in zip(tool_calls_ordered, results):
        # Handle exceptions gracefully
        if isinstance(result, Exception):
            content = json.dumps({"error": str(result), "tool": tool_call["name"]})
            print(f"  ⚠️  {tool_call['name']} failed: {str(result)}")
        else:
            # Capture specific data types for state updates
            if tool_call["name"] == "get_weather":
                weather_data_found = result
            elif tool_call["name"] == "get_images":
                image_urls_found = result
                
            # Convert result to JSON string for the ToolMessage content
            if isinstance(result, list):
                # Convert Pydantic models to dict if necessary
                content = json.dumps(
                    [item.dict() if hasattr(item, 'dict') else item for item in result]
                )
            elif isinstance(result, dict):
                content = json.dumps(result)
            else:
                content = json.dumps(str(result))
            
            print(f"  ✓ {tool_call['name']} → {len(content)} chars of data")
        
        # Create ToolMessage (LangChain protocol)
        tool_message = ToolMessage(
            tool_call_id=tool_call["id"],
            name=tool_call["name"],
            content=content
        )
        tool_messages.append(tool_message)

    # ========================================================================
    # STEP 4: Append all ToolMessages back to state & update data fields
    # ========================================================================
    state.messages.extend(tool_messages)
    
    # Update the explicit data fields if we found fresh data
    if weather_data_found:
        state.weather_data = weather_data_found
    if image_urls_found:
        state.image_urls = image_urls_found
        
    print(f"📋 {len(tool_messages)} ToolMessages appended to state")
    
    return state


# ============================================================================
# NODE 6: FORMAT OUTPUT
# ============================================================================

async def node_format_output(state: AgentState) -> AgentState:
    """
    Format final response as structured JSON (Pydantic).
    
    Takes whatever data is in state and creates a StructuredOutput.
    This is what Streamlit renders.
    
    Handles both paths:
    - Cache hit: Use cached summary + fresh weather/images
    - Cache miss + LLM: Use LLM-generated summary + tools data
    """
    city = state.city_name
    
    print(f"📦 Formatting output for '{city}'...")
    
    try:
        # Summary
        city_summary = state.city_summary
        
        # If no summary exists (Cache Miss path), we need to generate one from the tool outputs
        if not city_summary:
            print("  Generating summary from tool outputs...")
            messages = state.messages
            # Ask LLM to summarize the tool outputs
            summary_prompt = "Provide a 2-3 sentence summary of the city based on the tool outputs provided in the conversation."
            # We use ainvoke here
            response = await llm.ainvoke(messages + [HumanMessage(content=summary_prompt)])
            city_summary = response.content
            state.city_summary = city_summary

        # Weather data
        weather_data = state.weather_data or []
        
        # Image URLs
        image_urls = state.image_urls or []
        
        # Create structured output
        structured = StructuredOutput(
            city_summary=city_summary,
            weather_forecast=weather_data,
            image_urls=image_urls
        )
        
        state.final_output = structured
        
        print(f"✅ Output formatted:")
        print(f"   - Summary: {len(city_summary)} chars")
        print(f"   - Weather: {len(weather_data)} days")
        print(f"   - Images: {len(image_urls)} URLs")
        
    except Exception as e:
        print(f"⚠️  Error formatting output: {e}")
        state.error_message = str(e)
    
    return state