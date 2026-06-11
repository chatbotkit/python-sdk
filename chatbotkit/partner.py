from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class PartnerClient:
    def __init__(self, client: Client) -> None:
        self._client = client
        self.user = PartnerUserClient(client)


class PartnerUserClient:
    def __init__(self, client: Client) -> None:
        self._client = client
        self.token = PartnerUserTokenClient(client)

    def list(
        self,
        request: types.PartnerUserListParams | Request | None = None,
    ) -> Response[types.PartnerUserListResponse, types.PartnerUserListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/partner/user/list",
            query=request,
            parse=types.PartnerUserListResponse.from_dict,
            stream_parse=types.PartnerUserListStreamItem.from_dict,
        )

    def fetch(self, user_id: str) -> Response[types.PartnerUserFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/partner/user/{user_id}/fetch",
            parse=types.PartnerUserFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.PartnerUserCreateRequest | Request,
    ) -> Response[types.PartnerUserCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/partner/user/create",
            record=request,
            parse=types.PartnerUserCreateResponse.from_dict,
        )

    def update(
        self,
        user_id: str,
        request: types.PartnerUserUpdateRequest | Request,
    ) -> Response[types.PartnerUserUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/partner/user/{user_id}/update",
            record=request,
            parse=types.PartnerUserUpdateResponse.from_dict,
        )

    def delete(
        self,
        user_id: str,
        request: Request | None = None,
    ) -> Response[types.PartnerUserDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/partner/user/{user_id}/delete",
            record=request or {},
            parse=types.PartnerUserDeleteResponse.from_dict,
        )


class PartnerUserTokenClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        user_id: str,
        request: types.PartnerUserTokenListParams | Request | None = None,
    ) -> Response[
        types.PartnerUserTokenListResponse,
        types.PartnerUserTokenListStreamItem,
    ]:
        return self._client.client_fetch(
            f"/api/v1/partner/user/{user_id}/token/list",
            query=request,
            parse=types.PartnerUserTokenListResponse.from_dict,
            stream_parse=types.PartnerUserTokenListStreamItem.from_dict,
        )

    def create(
        self,
        user_id: str,
        request: types.PartnerUserTokenCreateRequest | Request,
    ) -> Response[types.PartnerUserTokenCreateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/partner/user/{user_id}/token/create",
            record=request,
            parse=types.PartnerUserTokenCreateResponse.from_dict,
        )

    def delete(
        self,
        user_id: str,
        token_id: str,
        request: Request | None = None,
    ) -> Response[types.PartnerUserTokenDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/partner/user/{user_id}/token/{token_id}/delete",
            record=request or {},
            parse=types.PartnerUserTokenDeleteResponse.from_dict,
        )
