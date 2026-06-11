from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class MemoryClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.MemoryListParams | Request | None = None,
    ) -> Response[types.MemoryListResponse, types.MemoryListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/memory/list",
            query=request,
            parse=types.MemoryListResponse.from_dict,
            stream_parse=types.MemoryListStreamItem.from_dict,
        )

    def fetch(self, memory_id: str) -> Response[types.MemoryFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/memory/{memory_id}/fetch",
            parse=types.MemoryFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.MemoryCreateRequest | Request,
    ) -> Response[types.MemoryCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/memory/create",
            record=request,
            parse=types.MemoryCreateResponse.from_dict,
        )

    def update(
        self,
        memory_id: str,
        request: types.MemoryUpdateRequest | Request,
    ) -> Response[types.MemoryUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/memory/{memory_id}/update",
            record=request,
            parse=types.MemoryUpdateResponse.from_dict,
        )

    def delete(
        self,
        memory_id: str,
        request: Request | None = None,
    ) -> Response[types.MemoryDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/memory/{memory_id}/delete",
            record=request or {},
            parse=types.MemoryDeleteResponse.from_dict,
        )

    def search(
        self,
        request: types.MemorySearchRequest | Request,
    ) -> Response[types.MemorySearchResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/memory/search",
            record=request,
            parse=types.MemorySearchResponse.from_dict,
        )

    def export(
        self,
        request: types.MemoriesExportParams | Request | None = None,
    ) -> Response[types.MemoriesExportResponse, types.MemoriesExportStreamItem]:
        return self._client.client_fetch(
            "/api/v1/memory/export",
            query=request,
            parse=types.MemoriesExportResponse.from_dict,
            stream_parse=types.MemoriesExportStreamItem.from_dict,
        )
