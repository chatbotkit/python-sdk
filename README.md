[![Follow on Twitter](https://img.shields.io/twitter/follow/chatbotkit.svg?logo=twitter)](https://twitter.com/chatbotkit)
[![ChatBotKit](https://img.shields.io/badge/credits-ChatBotKit-blue.svg)](https://chatbotkit.com)
[![CBK.AI](https://img.shields.io/badge/credits-CBK.AI-blue.svg)](https://cbk.ai)
[![Email](https://img.shields.io/badge/Email-Support-blue?logo=mail.ru)](mailto:support@chatbotkit.com)
[![Discord](https://img.shields.io/badge/Discord-Support-blue?logo=discord)](https://go.cbk.ai/discord)

```text
 .d8888b.  888888b.   888    d8P
d88P  Y88b 888  "88b  888   d8P
888    888 888  .88P  888  d8P
888        8888888K.  888d88K
888        888  "Y88b 8888888b
888    888 888    888 888  Y88b
Y88b  d88P 888   d88P 888   Y88b
 "Y8888P"  8888888P"  888    Y88b .ai
```

# ChatBotKit Python SDK

The official async Python SDK for [ChatBotKit](https://chatbotkit.com) - a platform
for building and deploying conversational AI applications. With ChatBotKit you can
swiftly develop and deploy AI bots and agents capable of natural language interactions.

## Why ChatBotKit?

**Build lighter, future-proof AI agents.** When you build with ChatBotKit, the heavy lifting happens on our servers-not in your application. This architectural advantage delivers:

- 🪶 **Lightweight Agents**: Your agents stay lean because complex AI processing, model orchestration, and tool execution happen server-side. Less code in your app means faster load times and simpler maintenance.

- 🛡️ **Robust & Streamlined**: Server-side processing provides a more reliable experience with built-in error handling, automatic retries, and consistent behavior across all platforms.

- 🔄 **Backward & Forward Compatible**: As AI technology evolves-new models, new capabilities, new paradigms-your agents automatically benefit. No code changes required on your end.

- 🔮 **Future-Proof**: Agents you build today will remain capable tomorrow. When we add support for new AI models or capabilities, your existing agents gain those powers without any updates to your codebase.

This means you can focus on building great user experiences while ChatBotKit handles the complexity of the ever-changing AI landscape.

## Installation

```bash
pip install chatbotkit
```

Requires Python 3.10 or later. The SDK is fully async and built on
[`httpx`](https://www.python-httpx.org/).

To use the optional agent helpers, install the agent extra:

```bash
pip install "chatbotkit[agent]"
```

Then import from `chatbotkit.agent`:

```python
from chatbotkit.agent import Tool, execute
```

## Development Checks

From `sdks/python`, run the same checks used by CI:

```bash
pip install -e ".[dev]"
python -m pytest tests
python -m compileall -q chatbotkit examples
python -m build
python -m twine check dist/*
```

The GitHub Actions workflow builds and checks publishable `sdist` and wheel
artifacts. Publishing is manual and disabled by default until PyPI trusted
publishing is configured.

## Quick Start

```python
import asyncio

from chatbotkit import ChatBotKit
from chatbotkit.types import ConversationCompleteStreamItemType


async def main():
    async with ChatBotKit(secret="your-api-key") as cbk:
        completion = cbk.conversation.complete(
            None,
            {
                "messages": [
                    {"type": "user", "text": "Hello! Tell me a joke."},
                ],
            },
        )

        async for event in completion.stream():
            if event.type == ConversationCompleteStreamItemType.TOKEN:
                print(event.data.token, end="", flush=True)


asyncio.run(main())
```

## SDK Client

Create a client with your API key and access resources as attributes:

```python
from chatbotkit import ChatBotKit

cbk = ChatBotKit(
    secret="your-api-key",
    base_url="https://api.chatbotkit.com",  # optional
    run_as_user_id="user-id",               # optional
    timezone="America/New_York",            # optional
)

cbk.bot              # Bot management
cbk.conversation     # Conversation management
cbk.dataset          # Dataset management (cbk.dataset.record)
cbk.skillset         # Skillset management (cbk.skillset.ability)
cbk.file             # File management
cbk.contact          # Contact management (cbk.contact.conversation/secret/space/task)
cbk.secret           # Secret management
cbk.memory           # Memory management
cbk.blueprint        # Blueprint management (cbk.blueprint.resource/bulletin)
cbk.task             # Task management (cbk.task.execution)
cbk.team             # Team management
cbk.space            # Space management (cbk.space.storage)
cbk.partner          # Partner management (cbk.partner.user.token)
cbk.policy           # Policy management
cbk.portal           # Portal management
cbk.usage            # Usage reporting (cbk.usage.series)
cbk.magic            # Magic AI generation (cbk.magic.prompt)
cbk.event            # Event log access (cbk.event.log)
cbk.graphql          # GraphQL operations
cbk.channel          # Channel publish/subscribe
cbk.platform         # Platform content (doc, example, manual, model, tutorial, ...)
cbk.integration      # Integrations (widget, slack, discord, whatsapp, telegram,
                     #   messenger, instagram, notion, sitemap, support, extract,
                     #   twilio, email, mcp_server, microsoft_teams, google_chat,
                     #   trigger)
```

The client manages an underlying `httpx.AsyncClient`. Use it as an async context
manager (`async with ChatBotKit(...) as cbk:`) or call `await cbk.aclose()` when you
are done to release the connection pool.

Every resource method returns an awaitable `Response`. `await` it to parse a normal
JSON response, or call `.stream()` to iterate over a JSONL stream:

```python
# Awaiting a response parses the JSON body into a typed object
bots = await cbk.bot.list({"take": 10})

# Streaming iterates over typed stream items as they arrive
async for item in cbk.bot.list({"take": 10}).stream():
    print(item.type, item.data.id)
```

Methods accept either a generated request/params object from `chatbotkit.types` or a
plain `dict`. Generated objects are serialized automatically.

## Resource Operations

### Bots

```python
# List bots
bots = await cbk.bot.list({"take": 10})

# Fetch a bot
bot = await cbk.bot.fetch("bot-id")

# Create a bot
bot = await cbk.bot.create({
    "name": "My Bot",
    "description": "A helpful assistant",
    "backstory": "You are a friendly AI assistant.",
})

# Update a bot
bot = await cbk.bot.update("bot-id", {"name": "Updated Bot Name"})

# Delete a bot
result = await cbk.bot.delete("bot-id")
```

### Conversations

```python
# Create a conversation
conversation = await cbk.conversation.create({})

# List conversations
conversations = await cbk.conversation.list({"take": 10})

# Continue an existing conversation
result = await cbk.conversation.complete("conversation-id", {
    "messages": [{"type": "user", "text": "Hello!"}],
})

# Or use the stateless endpoint by passing None as the conversation id
result = await cbk.conversation.complete(None, {
    "messages": [{"type": "user", "text": "Hello!"}],
})
```

### Datasets

```python
# Create a dataset
dataset = await cbk.dataset.create({"name": "Knowledge Base"})

# Add a record
record = await cbk.dataset.record.create("dataset-id", {
    "text": "Important information...",
})

# Search the dataset
results = await cbk.dataset.search("dataset-id", {"text": "search query"})
```

### Integrations

Each integration is reachable under `cbk.integration` and follows the same CRUD
shape, with a few integration-specific extras (`setup`, `initiate`, `sync`):

```python
# List Slack integrations
slack = await cbk.integration.slack.list({"take": 10})

# Create a widget integration
widget = await cbk.integration.widget.create({"name": "Website Widget"})

# Trigger a sync for a sitemap integration
await cbk.integration.sitemap.sync("integration-id")
```

The full list of resources is shown under [SDK Client](#sdk-client) above.

## Streaming

Completions and list endpoints support streaming. Call `.stream()` on the returned
`Response` to get an async iterator of typed stream items. Each item has a `type`
(an enum) and a `data` payload:

```python
from chatbotkit.types import ConversationCompleteStreamItemType

completion = cbk.conversation.complete(None, {
    "messages": [{"type": "user", "text": "Write a short poem."}],
})

async for event in completion.stream():
    if event.type == ConversationCompleteStreamItemType.TOKEN:
        print(event.data.token, end="", flush=True)
    elif event.type == ConversationCompleteStreamItemType.RESULT:
        print("\nDone!")
```

## Configuration Options

Options can be passed as keyword arguments or via a `ClientOptions` instance.

| Option                    | Description                                       |
| ------------------------- | ------------------------------------------------- |
| `secret`                  | API authentication token (required)               |
| `base_url`                | Custom API base URL                                |
| `run_as_user_id`          | Execute requests as a specific user                |
| `run_as_child_user_email` | Execute requests as a specific child user          |
| `timezone`                | Timezone for timestamp handling                    |
| `headers`                 | Extra headers to send with every request           |
| `timeout`                 | Request timeout in seconds                          |
| `transport`               | Custom `httpx` transport (useful for testing)      |

```python
from chatbotkit import ChatBotKit, ClientOptions

cbk = ChatBotKit(ClientOptions(secret="your-api-key", timezone="UTC"))
```

## Error Handling

Failed requests raise `APIError`, which carries the message, code, status, and URL
returned by the API:

```python
from chatbotkit import APIError

try:
    bot = await cbk.bot.fetch("invalid-id")
except APIError as error:
    print(error.status_code, error.code, error.message)
```

## Types

The `chatbotkit.types` module contains all request, response, and stream item types,
generated from the ChatBotKit OpenAPI specification. Each type provides `from_dict`
and `to_dict` helpers, and passing typed objects to resource methods is fully
supported:

```python
from chatbotkit.types import BotCreateRequest

bot = await cbk.bot.create(BotCreateRequest.from_dict({
    "name": "My Bot",
    "description": "Description",
}))
```

## Documentation

- **Platform Documentation**: Comprehensive guide to ChatBotKit [here](https://chatbotkit.com/docs).
- **Platform Tutorials**: Step-by-step tutorials for ChatBotKit [here](https://chatbotkit.com/tutorials).

## Contributing

Encounter a bug or want to contribute? Open an issue or submit a pull request on our
[official GitHub repository](https://github.com/chatbotkit).

`chatbotkit/types.py` is generated and should not be edited by hand. To regenerate it
from the latest API specification, run the type sync script from the platform repo:

```bash
pnpm --dir sites/main script:sync-types:python
```

Install the development dependencies and run the test suite with:

```bash
pip install -e ".[dev]"
pytest
```

## License

See [LICENSE](LICENSE) for details.
