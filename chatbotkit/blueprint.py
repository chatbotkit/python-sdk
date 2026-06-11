from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class BlueprintClient:
    def __init__(self, client: Client) -> None:
        self._client = client
        self.resource = BlueprintResourceClient(client)
        self.bulletin = BlueprintBulletinClient(client)

    def list(
        self,
        request: types.BlueprintListParams | Request | None = None,
    ) -> Response[types.BlueprintListResponse, types.BlueprintListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/blueprint/list",
            query=request,
            parse=types.BlueprintListResponse.from_dict,
            stream_parse=types.BlueprintListStreamItem.from_dict,
        )

    def fetch(self, blueprint_id: str) -> Response[types.BlueprintFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/blueprint/{blueprint_id}/fetch",
            parse=types.BlueprintFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.BlueprintCreateRequest | Request,
    ) -> Response[types.BlueprintCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/blueprint/create",
            record=request,
            parse=types.BlueprintCreateResponse.from_dict,
        )

    def update(
        self,
        blueprint_id: str,
        request: types.BlueprintUpdateRequest | Request,
    ) -> Response[types.BlueprintUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/blueprint/{blueprint_id}/update",
            record=request,
            parse=types.BlueprintUpdateResponse.from_dict,
        )

    def delete(
        self,
        blueprint_id: str,
        request: Request | None = None,
    ) -> Response[types.BlueprintDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/blueprint/{blueprint_id}/delete",
            record=request or {},
            parse=types.BlueprintDeleteResponse.from_dict,
        )


class BlueprintResourceClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        blueprint_id: str,
    ) -> Response[types.BlueprintResourceListResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/blueprint/{blueprint_id}/resource/list",
            parse=types.BlueprintResourceListResponse.from_dict,
        )


class BlueprintBulletinClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        blueprint_id: str,
        request: types.BlueprintBulletinListParams | Request | None = None,
    ) -> Response[
        types.BlueprintBulletinListResponse,
        types.BlueprintBulletinListStreamItem,
    ]:
        return self._client.client_fetch(
            f"/api/v1/blueprint/{blueprint_id}/bulletin/list",
            query=request,
            parse=types.BlueprintBulletinListResponse.from_dict,
            stream_parse=types.BlueprintBulletinListStreamItem.from_dict,
        )

    def create(
        self,
        blueprint_id: str,
        request: types.BlueprintBulletinCreateRequest | Request,
    ) -> Response[types.BlueprintBulletinCreateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/blueprint/{blueprint_id}/bulletin/create",
            record=request,
            parse=types.BlueprintBulletinCreateResponse.from_dict,
        )
