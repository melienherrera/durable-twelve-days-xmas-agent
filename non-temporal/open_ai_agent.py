import asyncio
from agents import Agent, Runner
from tools import sing_verse, get_gift_info


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
    tools=[sing_verse, get_gift_info]
)

async def main():
    print("""🎄 Welcome to the 12 Days of Christmas AI Agent! 🎵
    
You can ask questions like:
    🎁 Please sing the entire 12 Days of Christmas song for me!
    🎁 What gift comes on day 7?
    🎁 Sing days 1 through 5
    🎁 Tell me about the gift on day 5
""")
    user_request = input("What would you like to do?: ")
    result = await Runner.run(agent, user_request)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
