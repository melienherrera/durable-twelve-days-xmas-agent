"""
Starter script for the 12 Days of Christmas AI Agent.

This connects to Temporal and starts a workflow execution.
The workflow ID is important - using the same ID allows resuming after crashes!
"""

import asyncio
from temporalio.client import Client
from .workflow import TwelveDaysWorkflow
from temporalio.contrib.openai_agents import OpenAIAgentsPlugin
from temporalio.common import WorkflowIDReusePolicy
from dotenv import load_dotenv
import os


async def main():
    """Start the 12 Days of Christmas workflow."""
    # Load environment variables
    load_dotenv()
    
    client = await Client.connect(
        "localhost:7233",
        # Use the plugin to configure Temporal for use with OpenAI Agents SDK
        plugins=[OpenAIAgentsPlugin()],
    )
    
    # The user's request - change this to test different scenarios!
    print("""🎄 Welcome to the 12 Days of Christmas AI Agent! 🎵
    
You can ask questions like:
    🎁 Please sing the entire 12 Days of Christmas song for me!
    🎁 What gift comes on day 7?
    🎁 Sing days 1 through 5
    🎁 Tell me about the gift on day 5
""")
    user_request = input("What would you like to do?: ")
    
    print(f"\n{'='*60}")
    print(f"🎵 Starting 12 Days of Christmas Workflow")
    print(f"{'='*60}")
    print(f"📨 Request: {user_request}")
    print(f"{'='*60}\n")
    
    # Execute workflow
    result = await client.execute_workflow(
        TwelveDaysWorkflow.run,
        user_request,
        id="twelve-days-demo",  # Same ID = resume capability!
        task_queue="twelve-days-queue",
        id_reuse_policy=WorkflowIDReusePolicy.TERMINATE_IF_RUNNING,
    )
    
    print(f"\n{'='*60}")
    print(f"🎉 Workflow Completed Successfully!")
    print(f"{'='*60}")
    print(f"📝 Final result: {result}")
    print(f"{'='*60}\n")



if __name__ == "__main__":
    asyncio.run(main())

