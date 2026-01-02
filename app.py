import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime

# Import your graph logic directly
from graph_logic import create_graph


# Load environment variables
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="groq-langgraph-researcher",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for Polish (FIXED COLORS) ---
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    /* FIXED: Added 'color: #000000' to force black text on light backgrounds */
    .step-box {
        background-color: #f8f9fa;
        color: #000000; 
        border-left: 4px solid #1E88E5;
        padding: 1rem;
        margin-bottom: 0.8rem;
        border-radius: 4px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .success-box {
        background-color: #e8f5e9;
        color: #000000;
        border-left: 4px solid #4CAF50;
        padding: 1.5rem;
        border-radius: 4px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .query-display {
        background-color: #fff3e0;
        color: #000000;
        border-left: 4px solid #FF9800;
        padding: 1rem;
        border-radius: 4px;
        font-weight: 500;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Configuration")

    # Dynamic API Key Handling
    if not os.getenv("GROQ_API_KEY"):
        st.warning("⚠️ GROQ_API_KEY missing in .env")
        groq_key = st.text_input("Enter Groq API Key", type="password")
        if groq_key:
            os.environ["GROQ_API_KEY"] = groq_key

    if not os.getenv("TAVILY_API_KEY"):
        st.warning("⚠️ TAVILY_API_KEY missing in .env")
        tavily_key = st.text_input("Enter Tavily API Key", type="password")
        if tavily_key:
            os.environ["TAVILY_API_KEY"] = tavily_key

    st.divider()

    st.header("ℹ️ How it Works")
    st.markdown(
        """
    1. **Analyze**: AI decides if web search is needed.
    2. **Search**: Uses Tavily for real-time data if required.
    3. **Synthesize**: Compiles findings into a clear answer.
    """
    )

    st.divider()
    st.caption("Powered by LangGraph, Groq & Tavily")

# --- Main Interface ---
st.markdown(
    '<div class="main-header">🔍 groq-langgraph-researcher </div>', unsafe_allow_html=True
)
st.markdown(
    '<div class="sub-header">Your intelligent partner for deep research and quick answers.</div>',
    unsafe_allow_html=True,
)

# Initialize Session State
if "history" not in st.session_state:
    st.session_state.history = []

# Input Area
col1, col2 = st.columns([3, 1])

with col1:
    user_query = st.text_area(
        "What would you like to research?",
        placeholder="e.g., What are the latest breakthroughs in Quantum Computing?",
        height=100,
    )

with col2:
    st.write("")  # Spacer
    st.write("")  # Spacer
    run_button = st.button(
        "🚀 Start Research", type="primary", use_container_width=True
    )
    clear_button = st.button("🗑️ Clear History", use_container_width=True)

if clear_button:
    st.session_state.history = []
    st.rerun()

# --- Logic Execution ---
if run_button and user_query:
    if not os.getenv("GROQ_API_KEY") or not os.getenv("TAVILY_API_KEY"):
        st.error("❌ Please provide API Keys in the sidebar or .env file to proceed.")
    else:
        with st.spinner("🤖 Assistant is working..."):
            try:
                # Create and Run Graph
                graph = create_graph()

                initial_state = {
                    "query": user_query,
                    "needs_search": False,
                    "search_results": "",
                    "final_answer": "",
                    "steps": [],
                }

                # Invoke the LangGraph workflow
                result = graph.invoke(initial_state)

                # Display Results
                st.markdown("---")
                st.subheader("📝 Research Results")

                # Display Query
                st.markdown(
                    f'<div class="query-display"><strong>Query:</strong> {result["query"]}</div>',
                    unsafe_allow_html=True,
                )
                st.write("")

                # Display Steps Taken
                with st.expander("🔄 View Processing Steps", expanded=True):
                    for step in result.get("steps", []):
                        st.markdown(
                            f'<div class="step-box">{step}</div>',
                            unsafe_allow_html=True,
                        )

                # Display Final Answer
                st.markdown("### 💡 Answer")
                st.markdown(
                    f'<div class="success-box">{result["final_answer"]}</div>',
                    unsafe_allow_html=True,
                )

                # Save to History
                st.session_state.history.append(
                    {
                        "timestamp": datetime.now().strftime("%H:%M"),
                        "query": user_query,
                        "answer": result["final_answer"],
                        "steps": result["steps"],
                    }
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Check your API keys and internet connection.")

# --- History Section ---
if st.session_state.history:
    st.markdown("---")
    st.header("📜 Research History")

    # Reverse to show newest first
    for item in reversed(st.session_state.history):
        with st.expander(f"🕒 {item['timestamp']} - {item['query'][:60]}..."):
            st.markdown(f"**Query:** {item['query']}")
            st.markdown(f"**Answer:**\n{item['answer']}")
            st.caption(f"Steps taken: {len(item['steps'])}")
