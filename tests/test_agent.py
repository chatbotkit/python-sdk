from __future__ import annotations

import asyncio

import pytest

pydantic = pytest.importorskip("pydantic")

from chatbotkit.agent import Tool, complete, create_skills_feature, execute  # noqa: E402


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


class _FakeChannel:
    async def publish(self, channel, request):
        return {"id": channel}


def _tool_channels(record) -> dict[str, str]:
    return {f["name"]: f["result"]["channel"] for f in record["functions"]}


@pytest.mark.asyncio
async def test_execute_external_abort_signal_stops_before_first_call():
    class FakeClient:
        def __init__(self):
            self.channel = _FakeChannel()
            self.record = None
            self.calls = 0

        def client_fetch(self, path, **kwargs):
            self.calls += 1
            self.record = kwargs["record"]
            raise AssertionError("client_fetch must not run once aborted")

    client = FakeClient()
    abort_signal = asyncio.Event()
    abort_signal.set()

    events = [
        event
        async for event in execute(
            client=client,
            model="claude-4.5-sonnet",
            messages=[{"type": "user", "text": "go"}],
            abort_signal=abort_signal,
            max_iterations=5,
        )
    ]

    assert client.calls == 0
    assert events[-1] == {
        "type": "exit",
        "data": {"code": 1, "message": "Task execution aborted"},
    }


@pytest.mark.asyncio
async def test_execute_external_abort_mid_stream_cancels_iteration():
    abort_signal = asyncio.Event()
    consumed = 0

    class FakeResponse:
        def __init__(self, client):
            self.client = client

        async def stream(self):
            nonlocal consumed

            for index in range(6):
                if index == 2:
                    # an external actor (timeout, user) aborts mid-stream
                    abort_signal.set()

                consumed += 1

                yield {"type": "token", "data": {"token": "x"}}

                await asyncio.sleep(0)

    class FakeClient:
        def __init__(self):
            self.channel = _FakeChannel()
            self.record = None
            self.calls = 0

        def client_fetch(self, path, **kwargs):
            self.calls += 1
            self.record = kwargs["record"]

            return FakeResponse(self)

    client = FakeClient()

    events = [
        event
        async for event in execute(
            client=client,
            model="claude-4.5-sonnet",
            messages=[{"type": "user", "text": "go"}],
            abort_signal=abort_signal,
        )
    ]

    # the in-flight stream was cut short rather than draining all six tokens
    assert consumed < 6
    # and the loop did not start a second API iteration
    assert client.calls == 1
    assert events[-1] == {
        "type": "exit",
        "data": {"code": 1, "message": "Task execution aborted"},
    }


@pytest.mark.asyncio
async def test_execute_hard_abort_tool_cancels_iteration():
    consumed_after_abort = 0

    class FakeResponse:
        def __init__(self, client):
            self.client = client

        async def stream(self):
            nonlocal consumed_after_abort

            abort_channel = _tool_channels(self.client.record)["abort"]

            # the model calls abort(hard=True)
            yield {
                "type": "waitForChannelMessageBegin",
                "data": {
                    "channel": abort_channel,
                    "function": {"args": {"hard": True}},
                },
            }

            # give the abort tool task a turn to set the internal signal
            await asyncio.sleep(0)

            # these should not keep streaming once the hard abort fires
            for _ in range(5):
                consumed_after_abort += 1

                yield {"type": "token", "data": {"token": "x"}}

                await asyncio.sleep(0)

    class FakeClient:
        def __init__(self):
            self.channel = _FakeChannel()
            self.record = None

        def client_fetch(self, path, **kwargs):
            self.record = kwargs["record"]

            return FakeResponse(self)

    client = FakeClient()

    events = [
        event
        async for event in execute(
            client=client,
            model="claude-4.5-sonnet",
            messages=[{"type": "user", "text": "go"}],
        )
    ]

    assert consumed_after_abort < 5
    assert events[-1] == {
        "type": "exit",
        "data": {"code": 1, "message": "aborted by user request"},
    }
