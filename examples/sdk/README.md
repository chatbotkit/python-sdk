# ChatBotKit Python SDK Examples

These examples use the base `chatbotkit` package.

Install the example helper dependency:

```bash
pip install -e ".[examples]"
```

Set `CHATBOTKIT_API_SECRET` in the environment or in a `.env` file.

```bash
python3 examples/sdk/conversation_chat_stream.py
python3 examples/sdk/create_dataset.py
python3 examples/sdk/list_conversations.py
python3 examples/sdk/list_datasets_stream.py
```

Agent-specific examples live in `../agent`.
