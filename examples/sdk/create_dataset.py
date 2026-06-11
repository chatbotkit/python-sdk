from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv

from chatbotkit import ChatBotKit


async def main() -> None:
    load_dotenv()

    async with ChatBotKit(secret=os.environ["CHATBOTKIT_API_SECRET"]) as cbk:
        dataset = await cbk.dataset.create(
            {
                "name": "Python SDK Example Dataset",
                "description": "Created by the Python SDK examples",
            }
        )

        print(f"created dataset: {dataset.id}")

        record = await cbk.dataset.record.create(
            dataset.id,
            {
                "text": "ChatBotKit helps teams build conversational AI applications.",
                "source": "python-sdk-example",
            },
        )

        print(f"created record: {record.id}")

        results = await cbk.dataset.search(
            dataset.id,
            {"search": "conversational AI applications"},
        )

        print(f"search returned {len(results.records)} records")

        await cbk.dataset.delete(dataset.id)

        print(f"deleted dataset: {dataset.id}")


if __name__ == "__main__":
    asyncio.run(main())
