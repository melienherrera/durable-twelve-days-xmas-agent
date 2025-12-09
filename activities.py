"""
Tool implementations for the 12 Days of Christmas AI Agent.

These are Temporal activities that will be exposed to the OpenAI agent
as tools using the activity_as_tool helper function.
"""

import asyncio
from temporalio import activity

# The complete gift dictionary with emojis
GIFTS = {
    1: "🐦 A partridge in a pear tree",
    2: "🕊️ Two turtle doves",
    3: "🐔 Three French hens",
    4: "🐦 Four calling birds",
    5: "💍 FIVE GOLDEN RINGS",
    6: "🪿 Six geese a-laying",
    7: "🦢 Seven swans a-swimming",
    8: "🥛 Eight maids a-milking",
    9: "💃 Nine ladies dancing",
    10: "🤴 Ten lords a-leaping",
    11: "🎺 Eleven pipers piping",
    12: "🥁 Twelve drummers drumming"
}


@activity.defn
async def sing_verse(day: int) -> str:
    """Sings one verse of the 12 Days of Christmas song."""
    if day < 1 or day > 12:
        return f"Invalid day: {day}. Must be between 1 and 12."
    
    # Print the verse header
    print(f"\n🎵 On the {'first' if day == 1 else 'second' if day == 2 else 'third' if day == 3 else str(day) + 'th'} day of Christmas,")
    print(f"   my true love gave to me:")
    
    # Print the current day's gift
    print(f"   {GIFTS[day]}")
    
    # Print previous gifts in reverse order
    for prev_day in range(day - 1, 0, -1):
        gift = GIFTS[prev_day]
        # Add "and" before the partridge on multi-verse days
        if prev_day == 1 and day > 1:
            gift = "   And " + gift.lstrip("🐦 A").lstrip()
            print(f"   🐦 {gift}")
        else:
            print(f"   {gift}")
    
    #Simulate an error
    if day == 5:
        attempt = activity.info().attempt
        if attempt == 1:
            raise ApplicationError("I'm sorry, I made a mistake! I can't sing the 5th day of Christmas - let me try again!")
        elif attempt <= 3:
            await asyncio.sleep(10)
            raise ApplicationError("I'm sorry, I made a mistake! I can't sing the 5th day of Christmas - let me try again!")
    
    # Return statements reflect in the Temporal UI for tracking activity output
    return f"✓ Completed verse {day}: {GIFTS[day]}"


@activity.defn
async def get_gift_info(day: int) -> str:
    """Returns information about what gift comes on a specific day."""
    if day < 1 or day > 12:
        return f"Invalid day: {day}. Must be between 1 and 12."
    
    gift = GIFTS[day]
    print(f"On day {day}, the gift is: {gift}")
    
    # Return statements reflect in the Temporal UI
    return f"On day {day}, the gift is: {gift}"

