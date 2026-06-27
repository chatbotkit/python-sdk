from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, replace
from enum import Enum
from typing import Any, AsyncIterator, Callable, Generic, Mapping, TypeVar, cast

import httpx

T = TypeVar("T")
U = TypeVar("U")

Parser = Callable[[Any], T]


def _identity(value: Any) -> Any:
    return value


def _to_payload(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value

    if hasattr(value, "to_dict") and callable(value.to_dict):
        return value.to_dict()

    if isinstance(value, Mapping):
        return {key: _to_payload(item) for key, item in value.items()}

    if isinstance(value, (list, tuple)):
        return [_to_payload(item) for item in value]

    return value


def _to_query_value(value: Any) -> str:
    value = _to_payload(value)

    if isinstance(value, bool):
        return "true" if value else "false"

    return str(value)


def _query_items(query: Any) -> list[tuple[str, str]]:
    if query is None:
        return []

    query = _to_payload(query)

    if not isinstance(query, Mapping):
        raise TypeError("query must be a mapping or generated params object")

    items: list[tuple[str, str]] = []

    for key, value in query.items():
        if value is None:
            continue

        if isinstance(value, Mapping):
            for sub_key, sub_value in value.items():
                if sub_value is not None:
                    items.append((f"{key}.{sub_key}", _to_query_value(sub_value)))
        else:
            items.append((str(key), _to_query_value(value)))

    return items


@dataclass(frozen=True)
class ClientOptions:
    secret: str | None = None
    base_url: str = "https://api.chatbotkit.com"
    endpoints: Mapping[str, str] | None = None
    run_as_user_id: str | None = None
    run_as_child_user_email: str | None = None
    timezone: str | None = None
    headers: Mapping[str, str] | None = None
    timeout: float | None = None
    transport: httpx.AsyncBaseTransport | None = None


class APIError(Exception):
    def __init__(
        self,
        message: str,
        code: str | None = None,
        status_code: int | None = None,
        url: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.url = url


class Response(Generic[T, U]):
    def __init__(
        self,
        client: Client,
        path: str,
        *,
        method: str | None = None,
        query: Any = None,
        record: Any = None,
        headers: Mapping[str, str] | None = None,
        endpoint: str | None = None,
        parse: Parser[T] | None = None,
        stream_parse: Parser[U] | None = None,
    ) -> None:
        self._client = client
        self._path = path
        self._method = method
        self._query = query
        self._record = record
        self._headers = headers
        self._endpoint = endpoint
        self._parse = parse or cast(Parser[T], _identity)
        self._stream_parse = stream_parse or cast(Parser[U], _identity)
        self._task: asyncio.Task[T] | None = None

    def __await__(self) -> Any:
        return self.json().__await__()

    async def json(self) -> T:
        if self._task is None:
            self._task = asyncio.create_task(self._load_json())

        return await self._task

    async def _load_json(self) -> T:
        response = await self._client.request(
            self._path,
            method=self._method,
            query=self._query,
            record=self._record,
            headers=self._headers,
            endpoint=self._endpoint,
        )

        if not response.content:
            return self._parse(None)

        return self._parse(response.json())

    async def stream(self) -> AsyncIterator[U]:
        async with self._client.stream(
            self._path,
            method=self._method,
            query=self._query,
            record=self._record,
            headers=self._headers,
            endpoint=self._endpoint,
        ) as response:
            await self._client.raise_for_status(response)

            async for line in response.aiter_lines():
                line = line.strip()

                if not line:
                    continue

                yield self._stream_parse(json.loads(line))

    async def cache(self, key: str = "default") -> T:
        return await self._client.cache(self, key)

    def cache_key(self, key: str) -> str:
        return json.dumps(
            {
                "key": key,
                "method": self._method,
                "path": self._path,
                "query": _to_payload(self._query),
                "record": _to_payload(self._record),
            },
            sort_keys=True,
            default=str,
        )


class Client:
    def __init__(self, options: ClientOptions | None = None, **kwargs: Any) -> None:
        if options is not None and kwargs:
            raise TypeError("pass either ClientOptions or keyword options, not both")

        if options is None:
            options = ClientOptions(**kwargs)

        self.options = options
        self._base_url = httpx.URL(options.base_url)
        self._endpoints = dict(options.endpoints or {})
        self._headers = dict(options.headers or {})
        self._cache: dict[str, asyncio.Task[Any]] = {}
        self._http = httpx.AsyncClient(
            timeout=options.timeout,
            transport=options.transport,
        )

    def extend(self, **kwargs: Any) -> Client:
        return type(self)(replace(self.options, **kwargs))

    async def __aenter__(self) -> Client:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self._http.aclose()

    def client_fetch(
        self,
        path: str,
        *,
        method: str | None = None,
        query: Any = None,
        record: Any = None,
        headers: Mapping[str, str] | None = None,
        endpoint: str | None = None,
        parse: Parser[T] | None = None,
        stream_parse: Parser[U] | None = None,
    ) -> Response[T, U]:
        return Response(
            self,
            path,
            method=method,
            query=query,
            record=record,
            headers=headers,
            endpoint=endpoint,
            parse=parse,
            stream_parse=stream_parse,
        )

    async def cache(self, response: Response[T, Any], key: str) -> T:
        cache_key = response.cache_key(key)

        if cache_key not in self._cache:
            self._cache[cache_key] = asyncio.create_task(response.json())

        return cast(T, await self._cache[cache_key])

    async def request(
        self,
        path: str,
        *,
        method: str | None = None,
        query: Any = None,
        record: Any = None,
        headers: Mapping[str, str] | None = None,
        endpoint: str | None = None,
        raw: bool = False,
    ) -> httpx.Response:
        request = self._build_request(
            path,
            method=method,
            query=query,
            record=record,
            headers=headers,
            endpoint=endpoint,
        )

        response = await self._http.request(**request)

        # in raw (passthrough) mode the caller wants the response verbatim - do
        # not raise on a non-2xx status (e.g. the proxy's 409 authorization_required)
        if not raw:
            await self.raise_for_status(response)

        return response

    def stream(
        self,
        path: str,
        *,
        method: str | None = None,
        query: Any = None,
        record: Any = None,
        headers: Mapping[str, str] | None = None,
        endpoint: str | None = None,
    ) -> Any:
        request = self._build_request(
            path,
            method=method,
            query=query,
            record=record,
            headers={
                "accept": "application/jsonl",
                **dict(headers or {}),
            },
            endpoint=endpoint,
        )

        return self._http.stream(**request)

    def _build_request(
        self,
        path: str,
        *,
        method: str | None,
        query: Any,
        record: Any,
        headers: Mapping[str, str] | None,
        endpoint: str | None,
    ) -> dict[str, Any]:
        payload = _to_payload(record)
        method = method or ("POST" if record is not None else "GET")
        request_headers = self._build_headers(headers, has_body=record is not None)

        request: dict[str, Any] = {
            "method": method,
            "url": self._build_url(path, endpoint),
            "headers": request_headers,
            "params": _query_items(query),
        }

        if record is not None:
            request["json"] = payload

        return request

    def _build_url(self, path: str, endpoint: str | None) -> httpx.URL:
        target = self._endpoints.get(endpoint or path, path)

        if target.startswith(("http://", "https://")):
            url = httpx.URL(target)
        else:
            url = httpx.URL(f"{str(self._base_url).rstrip('/')}/{target.lstrip('/')}")

        if url.host == "api.chatbotkit.com" and url.path.startswith("/api/"):
            url = url.copy_with(path=url.path[4:])

        return url

    def _build_headers(
        self,
        headers: Mapping[str, str] | None,
        *,
        has_body: bool,
    ) -> dict[str, str]:
        result = {
            "accept": "application/json",
            **self._headers,
        }

        if has_body:
            result["content-type"] = "application/json"

        if self.options.secret:
            result["authorization"] = f"Bearer {self.options.secret}"

        if self.options.run_as_user_id:
            result["x-runas-user-id"] = self.options.run_as_user_id

        if self.options.run_as_child_user_email:
            result["x-runas-child-user-email"] = self.options.run_as_child_user_email

        if self.options.timezone:
            result["x-timezone"] = self.options.timezone

        result.update(headers or {})

        return result

    async def raise_for_status(self, response: httpx.Response) -> None:
        if response.status_code < 400:
            return

        message = f"HTTP Error: {response.reason_phrase}"
        code = f"ERROR_{response.status_code}"

        try:
            data = response.json()
            message = data.get("message") or message
            code = data.get("code") or code
        except ValueError:
            body = await response.aread()
            message = body.decode() or f"HTTP Error: {response.status_code}"

        raise APIError(
            message,
            code=code,
            status_code=response.status_code,
            url=str(response.url),
        )
