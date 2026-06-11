from __future__ import annotations

import json

import httpx
import pytest

from chatbotkit import APIError, ChatBotKit, ClientOptions


def make_client(handler, **options):
    transport = httpx.MockTransport(handler)
    return ChatBotKit(secret="cbk_test", transport=transport, **options)


@pytest.mark.asyncio
async def test_get_request_building():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["method"] = request.method
        captured["auth"] = request.headers.get("authorization")
        return httpx.Response(200, json={"ok": True})

    async with make_client(handler) as cbk:
        # exercise the transport directly with an identity parser
        await cbk.client_fetch("/api/v1/bot/bot_1/fetch", parse=lambda d: d)

    assert captured["method"] == "GET"
    # the /api prefix is stripped for api.chatbotkit.com
    assert captured["url"] == "https://api.chatbotkit.com/v1/bot/bot_1/fetch"
    assert captured["auth"] == "Bearer cbk_test"


@pytest.mark.asyncio
async def test_fetch_parses_json_into_typed_object():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "id": "bot_1",
                "name": "My Bot",
                "createdAt": 1700000000,
                "updatedAt": 1700000001,
            },
        )

    async with make_client(handler) as cbk:
        bot = await cbk.bot.fetch("bot_1")

    assert bot.id == "bot_1"
    assert bot.name == "My Bot"


@pytest.mark.asyncio
async def test_create_sends_json_body_and_post_method():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["body"] = json.loads(request.content)
        captured["content_type"] = request.headers.get("content-type")
        return httpx.Response(200, json={"id": "bot_2"})

    async with make_client(handler) as cbk:
        bot = await cbk.bot.create({"name": "New Bot", "model": "gpt-4o"})

    assert captured["method"] == "POST"
    assert captured["content_type"] == "application/json"
    assert captured["body"] == {"name": "New Bot", "model": "gpt-4o"}
    assert bot.id == "bot_2"


@pytest.mark.asyncio
async def test_list_query_params_are_serialized():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json={"items": []})

    async with make_client(handler) as cbk:
        await cbk.client_fetch(
            "/api/v1/bot/list",
            query={"take": 10, "meta": {"app": "record"}},
            parse=lambda d: d,
        )

    assert captured["params"]["take"] == "10"
    # nested mappings are flattened with dotted keys
    assert captured["params"]["meta.app"] == "record"


@pytest.mark.asyncio
async def test_stream_parses_jsonl_rows():
    rows = [
        {"type": "token", "data": {"token": "Hel"}},
        {"type": "token", "data": {"token": "lo"}},
        {"type": "result", "data": {"text": "Hello"}},
    ]

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers.get("accept") == "application/jsonl"
        body = "\n".join(json.dumps(r) for r in rows) + "\n"
        return httpx.Response(200, text=body)

    tokens = []
    async with make_client(handler) as cbk:
        completion = cbk.conversation.complete(
            None, {"messages": [{"type": "user", "text": "hi"}]}
        )
        async for event in completion.stream():
            if event.type.value == "token":
                tokens.append(event.data.token)

    assert tokens == ["Hel", "lo"]


@pytest.mark.asyncio
async def test_error_response_raises_api_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            404, json={"message": "Bot not found", "code": "NOT_FOUND"}
        )

    async with make_client(handler) as cbk:
        with pytest.raises(APIError) as info:
            await cbk.bot.fetch("missing")

    error = info.value
    assert error.status_code == 404
    assert error.code == "NOT_FOUND"
    assert error.message == "Bot not found"


@pytest.mark.asyncio
async def test_runas_and_timezone_headers():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["runas"] = request.headers.get("x-runas-user-id")
        captured["tz"] = request.headers.get("x-timezone")
        return httpx.Response(200, json={"id": "bot_1"})

    async with make_client(
        handler, run_as_user_id="user_9", timezone="UTC"
    ) as cbk:
        await cbk.client_fetch("/api/v1/bot/bot_1/fetch", parse=lambda d: d)

    assert captured["runas"] == "user_9"
    assert captured["tz"] == "UTC"


@pytest.mark.asyncio
async def test_nested_resource_routing():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        return httpx.Response(200, json={"id": "rec_1"})

    async with make_client(handler) as cbk:
        await cbk.dataset.record.create("ds_1", {"text": "hello"})

    assert captured["url"].endswith("/v1/dataset/ds_1/record/create")


def test_options_and_kwargs_are_mutually_exclusive():
    with pytest.raises(TypeError):
        ChatBotKit(ClientOptions(secret="a"), secret="b")
