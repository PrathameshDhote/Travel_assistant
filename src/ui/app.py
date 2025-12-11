import streamlit as st
import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import plotly.graph_objects as go
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

# Add the project root to sys.path so we can import from src
# This assumes app.py is in src/ui/
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import project modules
# These imports must happen after sys.path update
try:
    from src.vector_store.setup import populate_vector_store
    from src.graph.graph_builder import build_travel_graph
    from src.graph.state import AgentState
except ImportError as e:
    st.error(f"Import Error: {e}. Please ensure you are running from the project root.")
    st.stop()

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Travel Assistant",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SESSION STATE INITIALIZATION ---
def initialize_session_state():
    """Initialize Streamlit session variables for memory and history."""
    if "thread_id" not in st.session_state:
        # Unique ID for the conversation thread (required for Checkpointer)
        st.session_state.thread_id = f"user_{int(datetime.now().timestamp())}"
    
    if "history" not in st.session_state:
        st.session_state.history = []
        
    if "last_result" not in st.session_state:
        st.session_state.last_result = None

# --- CACHED RESOURCES ---
@st.cache_resource
def get_system_resources():
    """
    Initialize the Vector Store and Graph once and cache them.
    This prevents reloading the database on every interaction.
    """
    try:
        # 1. Initialize Vector Store (ChromaDB)
        client, collection = populate_vector_store()
        
        # 2. Build Graph (LangGraph)
        graph = build_travel_graph(collection)
        
        return graph, collection
    except Exception as e:
        st.error(f"Critical System Error: Failed to initialize resources. {e}")
        return None, None

# --- ASYNC HELPER ---
async def run_graph_async(graph, inputs, config):
    """
    Asynchronous wrapper to invoke the LangGraph agent.
    This is required because our graph nodes are async (for parallel tool execution).
    """
    return await graph.ainvoke(inputs, config=config)

# --- UI COMPONENTS ---
def display_weather_chart(weather_data):
    """Render an interactive Plotly line chart for weather."""
    if not weather_data:
        return

    try:
        # Extract data for plotting
        dates = [d.date for d in weather_data]
        temps = [d.temperature for d in weather_data]
        conditions = [d.condition for d in weather_data]

        # Create Plotly Figure
        fig = go.Figure()
        
        # Add Temperature Line
        fig.add_trace(go.Scatter(
            x=dates, 
            y=temps,
            mode='lines+markers',
            name='Temperature (°C)',
            line=dict(color='#FF4B4B', width=3),
            marker=dict(size=8),
            text=conditions,  # Show condition on hover
            hovertemplate='%{y}°C - %{text}'
        ))

        fig.update_layout(
            title="7-Day Temperature Forecast",
            xaxis_title="Date",
            yaxis_title="Temperature (°C)",
            template="plotly_white",
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, width="stretch")
    except Exception as e:
        st.warning(f"Could not render weather chart: {e}")

def display_image_gallery(image_urls):
    """Render a grid of images."""
    if not image_urls:
        return

    st.subheader("📸 City Gallery")
    cols = st.columns(min(3, len(image_urls)))
    for idx, url in enumerate(image_urls):
        with cols[idx % len(cols)]:
            try:
                st.image(url, width='stretch', caption=f"Image {idx+1}")
            except:
                st.warning("Image failed to load")

def display_final_output(result):
    """Parse and display the Structured Output from the agent."""
    
    # 1. Get the structured Pydantic object from state
    final_output = result.get("final_output")
    city_name = result.get("city_name", "Unknown City")
    is_cache_hit = result.get("vector_store_match", False)

    st.divider()
    
    # 2. Header & Status
    col_header, col_status = st.columns([3, 1])
    with col_header:
        st.header(f"📍 {city_name}")
    with col_status:
        if is_cache_hit:
            st.success("⚡ Data Source: Local Cache (Fast)")
        else:
            st.info("🌐 Data Source: Live Web Search")

    if not final_output:
        st.warning("No structured data was generated. The agent might have encountered an error.")
        if result.get("error_message"):
            st.error(f"Error Details: {result.get('error_message')}")
        return

    # 3. City Summary
    st.subheader("📝 Summary")
    st.markdown(final_output.city_summary)

    # 4. Weather Section
    if final_output.weather_forecast:
        st.subheader("🌤️ Weather Forecast")
        display_weather_chart(final_output.weather_forecast)
    
    # 5. Image Gallery
    if final_output.image_urls:
        display_image_gallery(final_output.image_urls)

    # 6. Raw Data Expander (For debugging/verification)
    with st.expander("🔍 View Raw JSON Response"):
        st.json(final_output.dict())

# --- MAIN APP LOGIC ---
def main():
    initialize_session_state()
    
    # Check for API Key
    if not os.getenv("OPENAI_API_KEY"):
        st.warning("⚠️ OPENAI_API_KEY not found. Please set it in your .env file.")
        st.stop()

    # Load System
    graph, collection = get_system_resources()
    
    if not graph:
        st.stop()

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Control Panel")
        st.write(f"**Session ID:** `{st.session_state.thread_id}`")
        
        if st.button("🧹 Clear Conversation History"):
            st.session_state.history = []
            st.session_state.last_result = None
            st.rerun()
            
        st.divider()
        st.markdown("### 🏙️ Pre-loaded Cities")
        st.caption("Try these for Cache Hits:")
        st.code("Paris\nTokyo\nNew York")

    # Main Input
    query = st.text_input("Where would you like to go?", placeholder="e.g., Tokyo, Snohomish, London...")
    
    if st.button("🚀 Plan Trip", type="primary") or query:
        if not query:
            st.warning("Please enter a city name.")
        else:
            with st.spinner("🤖 Agent is thinking... (Deciding between Cache vs. Web)"):
                try:
                    # Prepare Input State
                    initial_state = {
                        "messages": [HumanMessage(content=query)]
                    }
                    
                    # Config for Memory (Checkpointer)
                    config = {"configurable": {"thread_id": st.session_state.thread_id}}
                    
                    # --- CRITICAL FIX: EXECUTE ASYNC GRAPH ---
                    # We use asyncio.run() to bridge Streamlit (Sync) and LangGraph (Async)
                    result = asyncio.run(run_graph_async(graph, initial_state, config))
                    
                    # Update Session State
                    st.session_state.last_result = result
                    st.session_state.history.append({"query": query, "city": result.get("city_name")})
                    
                except Exception as e:
                    st.error(f"An error occurred during execution: {e}")
                    # Helpful debug info
                    import traceback
                    st.code(traceback.format_exc())

    # Display Result if exists
    if st.session_state.last_result:
        display_final_output(st.session_state.last_result)

if __name__ == "__main__":
    main()