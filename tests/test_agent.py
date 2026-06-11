from __future__ import annotations

import pytest

pydantic = pytest.importorskip("pydantic")

from chatbotkit.agent import Tool, complete, create_skills_feature  # noqa: E402


class WeatherInput(pydantic.BaseModel):
    location: str


async def get_weather(input: WeatherInput) -> dict[str, str]:
    return {"location": input.location}


def test_tool_function_definition_uses_pydantic_schema():
    tool = Tool(
        description="Get weather",
        input_model=WeatherInput,
        handler=get_weather,
    )

    definition = tool.function_definition("get_weather", "weather_channel")

    assert definition["name"] == "get_weather"
    assert definition["result"] == {"channel": "weather_channel"}
    assert definition["parameters"]["type"] == "object"
    assert "location" in definition["parameters"]["properties"]


def test_create_skills_feature():
    feature = create_skills_feature([])

    assert feature == {"name": "skills", "options": {"skills": []}}


@pytest.mark.asyncio
async def test_complete_runs_tool_and_publishes_result():
    class FakeChannel:
        def __init__(self):
            self.published = []

        async def publish(self, channel, request):
            self.published.append((channel, request))

            return {"id": channel}

    class FakeResponse:
        def __init__(self, client):
            self.client = client

        async def stream(self):
            channel = self.client.record["functions"][0]["result"]["channel"]

            yield {
                "type": "waitForChannelMessageBegin",
                "data": {
                    "channel": channel,
                    "function": {"args": {"location": "San Francisco, CA"}},
                },
            }
            yield {"type": "result", "data": {"end": {"reason": "stop"}}}

    class FakeClient:
        def __init__(self):
            self.channel = FakeChannel()
            self.record = None

        def client_fetch(self, path, **kwargs):
            self.path = path
            self.record = kwargs["record"]

            return FakeResponse(self)

    client = FakeClient()
    tool = Tool(
        description="Get weather",
        input_model=WeatherInput,
        handler=get_weather,
    )

    events = [
        event
        async for event in complete(
            client=client,
            model="claude-4.5-sonnet",
            messages=[{"type": "user", "text": "weather?"}],
            tools={"get_weather": tool},
        )
    ]

    assert client.path == "/api/v1/conversation/complete"
    assert client.record["limits"] == {"iterations": 1}
    assert events[0]["type"] == "toolCallStart"
    assert events[-1]["type"] == "toolCallEnd"
    assert client.channel.published == [
        (
            client.record["functions"][0]["result"]["channel"],
            {"message": {"data": {"location": "San Francisco, CA"}}},
        )
    ]
