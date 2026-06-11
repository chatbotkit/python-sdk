from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv

from chatbotkit import ChatBotKit


async def main() -> None:
    load_dotenv()

    async with ChatBotKit(secret=os.environ["CHATBOTKIT_API_SECRET"]) as cbk:
        async for event in cbk.dataset.list({"take": 10}).stream():
            if event.type.value != "item":
                continue

            print(f"{event.data.id}: {event.data.name}")


if __name__ == "__main__":
    asyncio.run(main())
