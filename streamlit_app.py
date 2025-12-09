"""
Streamlit UI for the 12 Days of Christmas AI Agent.

A simple web interface that provides the same functionality as the CLI
with a more digestible, holiday-themed presentation.
"""

import asyncio
import streamlit as st
from temporalio.client import Client
from temporalio.contrib.openai_agents import OpenAIAgentsPlugin
from temporalio.common import WorkflowIDReusePolicy
from workflow import TwelveDaysWorkflow
from dotenv import load_dotenv
import os

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
st.markdown("---")

# Welcome message with examples
with st.expander("ℹ️ What can you ask?", expanded=True):
    st.markdown("""
    Here are some things you can try:
    
    🎁 **Please sing the entire 12 Days of Christmas song for me!**
    
    🎁 **What gift comes on day 7?**
    
    🎁 **Sing days 1 through 5**
    
    🎁 **Tell me about the gift on day 5**
    """)

# Initialize session state
if 'result' not in st.session_state:
    st.session_state.result = None
if 'processing' not in st.session_state:
    st.session_state.processing = False

# User input
user_request = st.text_input(
    "❓ What would you like to do?",
    placeholder="e.g., Sing the entire song for me!",
    key="user_input"
)

# Process button
if st.button("🎵 Submit", type="primary"):
    if user_request:
        st.session_state.processing = True
        st.session_state.result = None
        
        # Show processing message
        with st.spinner("🎅 Processing your request..."):
            async def run_workflow():
                """Connect to Temporal and execute the workflow."""
                client = await Client.connect(
                    "localhost:7233",
                    plugins=[OpenAIAgentsPlugin()],
                )
                
                result = await client.execute_workflow(
                    TwelveDaysWorkflow.run,
                    user_request,
                    id="twelve-days-demo",
                    task_queue="twelve-days-queue",
                    id_reuse_policy=WorkflowIDReusePolicy.TERMINATE_IF_RUNNING,
                )
                
                return result
            
            try:
                # Run the async workflow
                result = asyncio.run(run_workflow())
                st.session_state.result = result
                st.session_state.processing = False
            except Exception as e:
                st.session_state.result = f"❌ Error: {str(e)}"
                st.session_state.processing = False
    else:
        st.warning("⚠️ Please enter a request first!")

# Display result
if st.session_state.result:
    st.markdown("---")
    st.markdown("### 🎉 Response:")
    st.markdown(f"""
    <div class="success-box">
    {st.session_state.result}
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>🎄 Powered by Temporal & OpenAI Agents SDK 🎄</p>
    <p><em>This agent's execution is durable - it can resume even after crashes!</em></p>
</div>
""", unsafe_allow_html=True)

