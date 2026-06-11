from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class PortalClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.PortalListParams | Request | None = None,
    ) -> Response[types.PortalListResponse, types.PortalListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/portal/list",
            query=request,
            parse=types.PortalListResponse.from_dict,
            stream_parse=types.PortalListStreamItem.from_dict,
        )

    def fetch(self, portal_id: str) -> Response[types.PortalFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/portal/{portal_id}/fetch",
            parse=types.PortalFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.PortalCreateRequest | Request,
    ) -> Response[types.PortalCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/portal/create",
            record=request,
            parse=types.PortalCreateResponse.from_dict,
        )

    def update(
        self,
        portal_id: str,
        request: types.PortalUpdateRequest | Request,
    ) -> Response[types.PortalUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/portal/{portal_id}/update",
            record=request,
            parse=types.PortalUpdateResponse.from_dict,
        )

    def delete(
        self,
        portal_id: str,
        request: Request | None = None,
    ) -> Response[types.PortalDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/portal/{portal_id}/delete",
            record=request or {},
            parse=types.PortalDeleteResponse.from_dict,
        )
