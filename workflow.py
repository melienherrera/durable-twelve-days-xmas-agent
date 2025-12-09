"""
Temporal workflow for the 12 Days of Christmas AI Agent.

This workflow uses the OpenAI Agents SDK integrated with Temporal to create
a durable AI agent. Each tool call runs as a Temporal activity, making the
entire agent interaction durable and observable.
"""

# Pre-import Pydantic dependencies to avoid sandbox warnings
# These must be imported BEFORE any workflow code to ensure they're loaded
# into Temporal's workflow sandbox properly
import annotated_types
import pydantic_core
import pydantic_core._pydantic_core
import pydantic_core.core_schema

from temporalio import workflow
from datetime import timedelta
from agents import Agent, Runner
from temporalio.contrib import openai_agents
from activities import sing_verse, get_gift_info

@workflow.defn
class TwelveDaysWorkflow:
    """
    Workflow that runs the 12 Days of Christmas AI agent.
    
    The key insight: Each tool call runs as a separate Temporal activity,
    so Temporal can checkpoint progress after each verse. If anything crashes,
    it resumes from the last completed verse.
    This is perfect for the 12 Days song - everyone forgets their place,
    but Temporal never does!
    """
    
    @workflow.run
    async def run(self, prompt: str) -> str:
        """
        Runs the AI agent to handle user requests about the song.
        The entire agent interaction is durable via Temporal.
        
        Args:
            prompt: The user's request (e.g., "Sing the whole song!")
            
        Returns:
            The agent's final response
        """
        print(f"\n{'='*60}")
        print(f"\n🎅 Starting 12 Days of Christmas Agent")
        # print(f"📝 User request: {prompt}\n")
        
        # Create the agent with activities as tools
        # activity_as_tool automatically generates OpenAI-compatible tool schemas
        # and wraps each activity call so Temporal can track and checkpoint them
        agent = Agent(
            name="twelve-days-teacher",
            model="gpt-4o",  # Use GPT-4o for better performance
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
            tools=[
                openai_agents.workflow.activity_as_tool(
                    sing_verse,
                    start_to_close_timeout=timedelta(seconds=10)
                ),
                openai_agents.workflow.activity_as_tool(
                    get_gift_info,
                    start_to_close_timeout=timedelta(seconds=5)
                )
            ]
        )
        
        # Run the agent - this handles the entire agent loop with durability
        result = await Runner.run(agent, prompt)
        
        print(f"\n✨ Agent completed successfully!")
        print(f"\n{'='*60}")
        
        # Return the agent's response
        # Note: The full verses are printed in the worker terminal by the activities
        return result.final_output

