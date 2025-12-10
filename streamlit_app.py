"""
Streamlit UI for the 12 Days of Christmas AI Agent.

A simple web interface that provides the same functionality as the CLI
with a more digestible, holiday-themed presentation.

Includes two tabs to compare:
- Temporal version (durable, resumable)
- Pure OpenAI Agents SDK (non-durable, loses context on crash)
"""

import asyncio
import streamlit as st
from temporalio.client import Client
from temporalio.contrib.openai_agents import OpenAIAgentsPlugin
from temporalio.common import WorkflowIDReusePolicy
from durable_temporal.workflow import TwelveDaysWorkflow
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# Add non-temporal directory to path for imports
non_temporal_path = Path(__file__).parent / "non-temporal"
sys.path.insert(0, str(non_temporal_path))

from agents import Agent, Runner
import tools as non_temporal_tools

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="12 Days of Christmas AI Agent",
    page_icon="🎄",
    layout="centered",
)

# Custom CSS for holiday theme
st.markdown("""
    <style>
    .main {
        background-color: #fafafa;
    }
    .stTextInput > div > div > input {
        border: 2px solid #c41e3a;
    }
    .stButton > button {
        background-color: #165b33;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        border: none;
    }
    .stButton > button:hover {
        background-color: #0f4027;
    }
    .success-box {
        background-color: #e8f5e9;
        border: 2px solid #165b33;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #1b5e20;
    }
    .info-box {
        background-color: #e8f4f8;
        border: 1px solid #bee5eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("# 🎄 12 Days of Christmas AI Agent 🎵")
st.markdown("Compare durable vs non-durable AI agents")

# Create tabs
tab1, tab2 = st.tabs(["🔄 Temporal (Durable)", "⚠️ Non-Temporal (Non-Durable)"])

# TAB 1: Temporal Version (Durable)
with tab1:
    st.markdown("### Temporal + OpenAI Agents SDK")
    st.success("✅ This version is **durable** - if the worker crashes, it resumes from the last checkpoint!")
    
    # Examples in a nice info container
    with st.container(border=True):
        st.markdown("**🎄 Try these examples:**")
        st.markdown("""
        - Please sing the entire 12 Days of Christmas song for me!
        - What gift comes on day 7?
        - Sing days 1 through 5
        - Tell me about the gift on day 5
        """)

    # Initialize session state
    if 'temporal_result' not in st.session_state:
        st.session_state.temporal_result = None
    if 'temporal_processing' not in st.session_state:
        st.session_state.temporal_processing = False

    # User input
    temporal_request = st.text_input(
        "❓ What would you like to do?",
        placeholder="e.g., Sing the entire song for me!",
        key="temporal_input"
    )

    # Process button
    if st.button("🎵 Submit", type="primary", key="temporal_submit"):
        if temporal_request:
            st.session_state.temporal_processing = True
            st.session_state.temporal_result = None
            
            # Show processing message
            with st.spinner("🎅 Processing your request with Temporal..."):
                async def run_workflow():
                    """Connect to Temporal and execute the workflow."""
                    client = await Client.connect(
                        "localhost:7233",
                        plugins=[OpenAIAgentsPlugin()],
                    )
                    
                    result = await client.execute_workflow(
                        TwelveDaysWorkflow.run,
                        temporal_request,
                        id="twelve-days-demo",
                        task_queue="twelve-days-queue",
                        id_reuse_policy=WorkflowIDReusePolicy.TERMINATE_IF_RUNNING,
                    )
                    
                    return result
                
                try:
                    # Run the async workflow
                    result = asyncio.run(run_workflow())
                    st.session_state.temporal_result = result
                    st.session_state.temporal_processing = False
                except Exception as e:
                    st.session_state.temporal_result = f"❌ Error: {str(e)}\n\nMake sure the Temporal server and worker are running!"
                    st.session_state.temporal_processing = False
        else:
            st.warning("⚠️ Please enter a request first!")

    # Display result
    if st.session_state.temporal_result:
        st.markdown("---")
        st.markdown("### 🎉 Response:")
        st.markdown(f"""
        <div class="success-box">
        {st.session_state.temporal_result}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("💡 **Tip**: Check your Worker terminal to see the full verses being printed. Try crashing the worker (Ctrl+C) and restarting it to see durability in action!")

# TAB 2: Non-Temporal Version (Non-Durable)
with tab2:
    st.markdown("### Pure OpenAI Agents SDK")
    st.warning("⚠️ This version is **NOT durable** - if this script crashes, all context is lost!")
    
    # Examples in a nice info container
    with st.container(border=True):
        st.markdown("**🎄 Try these examples:**")
        st.markdown("""
        - Please sing the entire 12 Days of Christmas song for me!
        - What gift comes on day 7?
        - Sing days 1 through 5
        - Tell me about the gift on day 5
        """)

    # Initialize session state
    if 'non_temporal_result' not in st.session_state:
        st.session_state.non_temporal_result = None
    if 'non_temporal_processing' not in st.session_state:
        st.session_state.non_temporal_processing = False

    # User input
    non_temporal_request = st.text_input(
        "❓ What would you like to do?",
        placeholder="e.g., Sing the entire song for me!",
        key="non_temporal_input"
    )

    # Process button
    if st.button("🎵 Submit", type="primary", key="non_temporal_submit"):
        if non_temporal_request:
            st.session_state.non_temporal_processing = True
            st.session_state.non_temporal_result = None
            
            # Show processing message
            with st.spinner("🎅 Processing your request with OpenAI Agents SDK..."):
                async def run_agent():
                    """Run the pure OpenAI agent."""
                    agent = Agent(
                        name="twelve-days-teacher",
                        model="gpt-4o",
                        instructions="""You are a cheerful AI teacher helping someone learn "The 12 Days of Christmas" song.

When asked to sing the ENTIRE/FULL/WHOLE song (all 12 days):
1. Call sing_verse for each day from 1 to 12 in order
2. Make sure to complete all 12 days - don't skip any!
3. After calling all the tools, provide a condensed summary listing each day with ONLY its main gift (not cumulative)
4. Format like: "On the first day of Christmas, my true love gave to me... 🐦 A partridge in a pear tree"
5. Then "On the second day of Christmas, my true love gave to me... 🕊️ Two turtle doves"
6. Continue through all 12 days in this condensed format

When asked to sing specific days or a range (like "day 7" or "days 1-5"):
1. Call sing_verse for each requested day
2. In your response, write out the FULL verses with all cumulative gifts as they appear in the song
3. Include all the previous gifts that come before, just like in the traditional song
4. Be enthusiastic and sing the complete verses!

When asked about specific gifts:
- Use get_gift_info to answer questions about what comes on which day
- Be helpful and enthusiastic

Always be enthusiastic and make learning fun! Use holiday emojis when appropriate.""",
                        tools=[non_temporal_tools.sing_verse, non_temporal_tools.get_gift_info]
                    )
                    result = await Runner.run(agent, non_temporal_request)
                    return result.final_output
                    
                try:
                    # Run the async agent
                    result = asyncio.run(run_agent())
                    st.session_state.non_temporal_result = result
                    st.session_state.non_temporal_processing = False
                except Exception as e:
                    st.session_state.non_temporal_result = f"❌ Error: {str(e)}"
                    st.session_state.non_temporal_processing = False
        else:
            st.warning("⚠️ Please enter a request first!")

    # Display result
    if st.session_state.non_temporal_result:
        st.markdown("---")
        st.markdown("### 🎉 Response:")
        st.markdown(f"""
        <div class="success-box">
        {st.session_state.non_temporal_result}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("⚠️ **Note**: This execution runs entirely in the Streamlit process. If you Ctrl+C this terminal, all progress is lost forever!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>🎄 Powered by Temporal & OpenAI Agents SDK 🎄</p>
    <p><em>This agent's execution is durable - it can resume even after crashes!</em></p>
</div>
""", unsafe_allow_html=True)

