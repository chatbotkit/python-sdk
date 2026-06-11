from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv

from chatbotkit import ChatBotKit


async def main() -> None:
    load_dotenv()

    messages: list[dict[str, str]] = []

    async with ChatBotKit(secret=os.environ["CHATBOTKIT_API_SECRET"]) as cbk:
        while True:
            text = input("user: ").strip()

            if text in {"exit", "quit"}:
                break

            messages.append({"type": "user", "text": text})
            print("bot: ", end="", flush=True)

            async for event in cbk.conversation.complete(
                None,
                {
                    "model": "gpt-4o",
                    "messages": messages,
                },
            ).stream():
                event_type = event.type.value

                if event_type == "token":
                    print(event.data.token, end="", flush=True)
                elif event_type == "result":
                    messages.append({"type": "bot", "text": event.data.text})

            print()


if __name__ == "__main__":
    asyncio.run(main())
