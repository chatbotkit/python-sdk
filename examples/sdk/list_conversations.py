from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv

from chatbotkit import ChatBotKit


async def main() -> None:
    load_dotenv()

    async with ChatBotKit(secret=os.environ["CHATBOTKIT_API_SECRET"]) as cbk:
        conversations = await cbk.conversation.list({"take": 10})

        for conversation in conversations.items:
            print(conversation.id)


if __name__ == "__main__":
    asyncio.run(main())
