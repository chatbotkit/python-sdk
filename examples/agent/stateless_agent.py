from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from chatbotkit import ChatBotKit
from chatbotkit.agent import Tool, execute


class WeatherInput(BaseModel):
    location: str = Field(description="The city and state, e.g. San Francisco, CA")


async def get_weather(input: WeatherInput) -> dict[str, object]:
    return {
        "location": input.location,
        "temperature": 72,
        "conditions": "sunny",
        "humidity": 45,
    }


async def main() -> None:
    load_dotenv()

    messages = [
        {
            "type": "user",
            "text": "What is the weather in San Francisco?",
        }
    ]

    async with ChatBotKit(secret=os.environ["CHATBOTKIT_API_SECRET"]) as cbk:
        async for event in execute(
            client=cbk,
            model="claude-4.5-sonnet",
            messages=messages,
            tools={
                "get_weather": Tool(
                    description="Get the current weather for a location",
                    input_model=WeatherInput,
                    handler=get_weather,
                )
            },
            max_iterations=10,
        ):
            event_type = event.get("type")

            if event_type == "iteration":
                print(f"\n[Iteration {event['data']['iteration']}]")
            elif event_type == "toolCallStart":
                print(f"Calling {event['data']['name']}: {event['data']['args']}")
            elif event_type == "token":
                print(event["data"]["token"], end="", flush=True)
            elif event_type == "exit":
                print(f"\nExit: {event['data']}")


if __name__ == "__main__":
    asyncio.run(main())
