from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class SpaceClient:
    def __init__(self, client: Client) -> None:
        self._client = client
        self.storage = SpaceStorageClient(client)

    def list(
        self,
        request: types.SpaceListParams | Request | None = None,
    ) -> Response[types.SpaceListResponse, types.SpaceListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/space/list",
            query=request,
            parse=types.SpaceListResponse.from_dict,
            stream_parse=types.SpaceListStreamItem.from_dict,
        )

    def fetch(self, space_id: str) -> Response[types.SpaceFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/space/{space_id}/fetch",
            parse=types.SpaceFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.SpaceCreateRequest | Request,
    ) -> Response[types.SpaceCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/space/create",
            record=request,
            parse=types.SpaceCreateResponse.from_dict,
        )

    def update(
        self,
        space_id: str,
        request: types.SpaceUpdateRequest | Request,
    ) -> Response[types.SpaceUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/space/{space_id}/update",
            record=request,
            parse=types.SpaceUpdateResponse.from_dict,
        )

    def delete(
        self,
        space_id: str,
        request: Request | None = None,
    ) -> Response[types.SpaceDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/space/{space_id}/delete",
            record=request or {},
            parse=types.SpaceDeleteResponse.from_dict,
        )


class SpaceStorageClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        space_id: str,
        request: types.SpaceStoragePathListParams | Request | None = None,
    ) -> Response[types.SpaceStoragePathListResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/space/{space_id}/storage/list",
            query=request,
            parse=types.SpaceStoragePathListResponse.from_dict,
        )

    def delete(
        self,
        space_id: str,
        path: str,
        request: types.SpaceStoragePathDeleteRequest | Request | None = None,
    ) -> Response[types.SpaceStoragePathDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/space/{space_id}/storage/delete/{path}",
            record=request or {},
            parse=types.SpaceStoragePathDeleteResponse.from_dict,
        )
