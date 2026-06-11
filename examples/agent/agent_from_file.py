from __future__ import annotations

import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

from chatbotkit import ChatBotKit
from chatbotkit.agent import execute, load_agent


async def main() -> None:
    load_dotenv()

    agent = load_agent(
        "assistant.md",
        roots=[str(Path(__file__).parent / "agents")],
    )

    messages = [
        {
            "type": "user",
            "text": "Write a three-bullet launch checklist.",
        }
    ]

    async with ChatBotKit(secret=os.environ["CHATBOTKIT_API_SECRET"]) as cbk:
        async for event in execute(
            client=cbk,
            model=agent.model or "gpt-4o",
            messages=messages,
            extensions={"backstory": agent.backstory},
            max_iterations=10,
        ):
            event_type = event.get("type")

            if event_type == "iteration":
                print(f"\n[Iteration {event['data']['iteration']}]")
            elif event_type == "token":
                print(event["data"]["token"], end="", flush=True)
            elif event_type == "exit":
                print(f"\nExit: {event['data']}")


if __name__ == "__main__":
    asyncio.run(main())
