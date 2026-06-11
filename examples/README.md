# ChatBotKit Python SDK Examples

This directory contains examples for the ChatBotKit Python SDK.

## Install

From `sdks/python`, install the SDK in editable mode:

```bash
pip install -e ".[examples,agent]"
```

Set your API key before running examples:

```bash
export CHATBOTKIT_API_SECRET="your-api-key"
```

You can also put the key in a `.env` file. The examples load it with
`python-dotenv`:

```bash
CHATBOTKIT_API_SECRET="your-api-key"
```

## Groups

- `sdk/` contains examples for the core `chatbotkit` package.
- `agent/` contains examples for the optional `chatbotkit[agent]` extra.

## Core SDK Examples

```bash
python3 examples/sdk/conversation_chat_stream.py
python3 examples/sdk/create_dataset.py
python3 examples/sdk/list_conversations.py
python3 examples/sdk/list_datasets_stream.py
```

## Agent Examples

```bash
python3 examples/agent/stateless_agent.py
python3 examples/agent/stateful_agent.py
python3 examples/agent/agent_with_tools.py
python3 examples/agent/agent_with_skills.py
python3 examples/agent/agent_from_file.py
```
