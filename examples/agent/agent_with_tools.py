from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from chatbotkit import ChatBotKit
from chatbotkit.agent import Tool, execute


class WeatherInput(BaseModel):
    location: str = Field(description="The city and state, e.g. San Francisco, CA")


class TimeInput(BaseModel):
    timezone: str = Field(description="The timezone, e.g. America/Los_Angeles")


async def get_weather(input: WeatherInput) -> dict[str, object]:
    return {
        "location": input.location,
        "temperature": 72,
        "conditions": "sunny",
        "humidity": 45,
    }


async def get_time(input: TimeInput) -> dict[str, object]:
    return {
        "timezone": input.timezone,
        "time": "2:30 PM",
        "date": "Monday, January 26, 2026",
    }


async def main() -> None:
    load_dotenv()

    messages = [
        {
            "type": "user",
            "text": (
                "What is the weather in San Francisco and what time is it in "
                "Los Angeles?"
            ),
        }
    ]

    tools = {
        "get_weather": Tool(
            description="Get the current weather for a location",
            input_model=WeatherInput,
            handler=get_weather,
        ),
        "get_time": Tool(
            description="Get the current time for a timezone",
            input_model=TimeInput,
            handler=get_time,
        ),
    }

    async with ChatBotKit(secret=os.environ["CHATBOTKIT_API_SECRET"]) as cbk:
        async for event in execute(
            client=cbk,
            model="claude-4.5-sonnet",
            messages=messages,
            tools=tools,
            max_iterations=10,
        ):
            event_type = event.get("type")

            if event_type == "toolCallStart":
                print(f"Calling {event['data']['name']}: {event['data']['args']}")
            elif event_type == "toolCallEnd":
                print(f"Completed {event['data']['name']}: {event['data']['result']}")
            elif event_type == "token":
                print(event["data"]["token"], end="", flush=True)
            elif event_type == "exit":
                print(f"\nExit: {event['data']}")


if __name__ == "__main__":
    asyncio.run(main())
