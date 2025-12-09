"""
Temporal worker for the 12 Days of Christmas AI Agent.

The worker listens for workflow tasks and executes them.
Run this in one terminal, then run starter.py in another to execute workflows.
"""

import asyncio
import os
from dotenv import load_dotenv
from datetime import timedelta
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio.contrib.openai_agents import OpenAIAgentsPlugin, ModelActivityParameters

from workflow import TwelveDaysWorkflow
from activities import sing_verse, get_gift_info


async def main():
    """Start the Temporal worker."""
    # Load environment variables from .env file
    load_dotenv()
    
    client = await Client.connect(
        "localhost:7233",
        plugins=[
            OpenAIAgentsPlugin(
                model_params=ModelActivityParameters(
                    start_to_close_timeout=timedelta(seconds=30)
                )
            ),
        ],
    )
    
    worker = Worker(
        client,
        task_queue="twelve-days-queue",
        workflows=[TwelveDaysWorkflow],
        activities=[sing_verse, get_gift_info],
    )
    
    print("\n" + "="*60)
    print("🎄 12 Days of Christmas Worker Started!")
    print("="*60)
    print("📋 Task queue: twelve-days-queue")
    print("🔄 Workflows: TwelveDaysWorkflow")
    print("🛠️  Activities: sing_verse, get_gift_info")
    print("\n✨ Waiting for workflows... (Press Ctrl+C to stop)")
    print("="*60 + "\n")
    
    # Run the worker (this blocks until interrupted)
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

