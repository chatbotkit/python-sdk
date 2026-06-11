from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class FileClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.FileListParams | Request | None = None,
    ) -> Response[types.FileListResponse, types.FileListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/file/list",
            query=request,
            parse=types.FileListResponse.from_dict,
            stream_parse=types.FileListStreamItem.from_dict,
        )

    def fetch(self, file_id: str) -> Response[types.FileFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/file/{file_id}/fetch",
            parse=types.FileFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.FileCreateRequest | Request,
    ) -> Response[types.FileCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/file/create",
            record=request,
            parse=types.FileCreateResponse.from_dict,
        )

    def update(
        self,
        file_id: str,
        request: types.FileUpdateRequest | Request,
    ) -> Response[types.FileUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/file/{file_id}/update",
            record=request,
            parse=types.FileUpdateResponse.from_dict,
        )

    def delete(
        self,
        file_id: str,
        request: Request | None = None,
    ) -> Response[types.FileDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/file/{file_id}/delete",
            record=request or {},
            parse=types.FileDeleteResponse.from_dict,
        )

    def sync(
        self,
        file_id: str,
        request: Request | None = None,
    ) -> Response[types.FileSyncResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/file/{file_id}/sync",
            record=request or {},
            parse=types.FileSyncResponse.from_dict,
        )
