from __future__ import annotations

from typing import Any

from . import types
from ._transport import Client, Response


class UsageClient:
    def __init__(self, client: Client) -> None:
        self._client = client
        self.series = UsageSeriesClient(client)

    def fetch(self) -> Response[types.UsageFetchResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/usage/fetch",
            parse=types.UsageFetchResponse.from_dict,
        )


class UsageSeriesClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def fetch(self) -> Response[types.UsageSeriesFetchResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/usage/series/fetch",
            parse=types.UsageSeriesFetchResponse.from_dict,
        )
