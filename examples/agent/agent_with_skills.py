from __future__ import annotations

import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

from chatbotkit import ChatBotKit
from chatbotkit.agent import create_skills_feature, execute, load_skills


async def main() -> None:
    load_dotenv()

    skills_result = load_skills([str(Path(__file__).parent / "skills")])
    skills_feature = create_skills_feature(skills_result.skills)

    messages = [
        {
            "type": "user",
            "text": "Use the summarize skill on: Python examples should be small, focused, and easy to run.",
        }
    ]

    async with ChatBotKit(secret=os.environ["CHATBOTKIT_API_SECRET"]) as cbk:
        async for event in execute(
            client=cbk,
            model="gpt-4o",
            messages=messages,
            extensions={"features": [skills_feature]},
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
