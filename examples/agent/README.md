# ChatBotKit Python Agent Examples

Install the optional agent dependencies before running these examples:

```bash
cd sdks/python
pip install -e ".[examples,agent]"
export CHATBOTKIT_API_SECRET="your-api-key"
```

You can also put `CHATBOTKIT_API_SECRET="your-api-key"` in a `.env` file.

Run an example:

```bash
python3 examples/agent/stateless_agent.py
python3 examples/agent/stateful_agent.py
python3 examples/agent/agent_with_tools.py
python3 examples/agent/agent_with_skills.py
python3 examples/agent/agent_from_file.py
```

## Examples

- `stateless_agent.py` runs an agent loop with local message history.
- `stateful_agent.py` runs an agent loop against a persisted conversation.
- `agent_with_tools.py` registers multiple local tools with typed inputs.
- `agent_with_skills.py` loads local `SKILL.md` files into a skills feature.
- `agent_from_file.py` loads an agent definition from markdown front matter.
