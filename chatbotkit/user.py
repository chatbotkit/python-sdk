from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class UserClient:
    def __init__(self, client: Client) -> None:
        self._client = client
        self.token = UserTokenClient(client)

    def list(
        self,
        request: types.UserListParams | Request | None = None,
    ) -> Response[types.UserListResponse, types.UserListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/user/list",
            query=request,
            parse=types.UserListResponse.from_dict,
            stream_parse=types.UserListStreamItem.from_dict,
        )

    def fetch(self, user_id: str) -> Response[types.UserFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/user/{user_id}/fetch",
            parse=types.UserFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.UserCreateRequest | Request,
    ) -> Response[types.UserCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/user/create",
            record=request,
            parse=types.UserCreateResponse.from_dict,
        )

    def update(
        self,
        user_id: str,
        request: types.UserUpdateRequest | Request,
    ) -> Response[types.UserUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/user/{user_id}/update",
            record=request,
            parse=types.UserUpdateResponse.from_dict,
        )

    def delete(
        self,
        user_id: str,
        request: Request | None = None,
    ) -> Response[types.UserDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/user/{user_id}/delete",
            record=request or {},
            parse=types.UserDeleteResponse.from_dict,
        )


class UserTokenClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        user_id: str,
        request: types.UserTokenListParams | Request | None = None,
    ) -> Response[
        types.UserTokenListResponse,
        types.UserTokenListStreamItem,
    ]:
        return self._client.client_fetch(
            f"/api/v1/user/{user_id}/token/list",
            query=request,
            parse=types.UserTokenListResponse.from_dict,
            stream_parse=types.UserTokenListStreamItem.from_dict,
        )

    def create(
        self,
        user_id: str,
        request: types.UserTokenCreateRequest | Request,
    ) -> Response[types.UserTokenCreateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/user/{user_id}/token/create",
            record=request,
            parse=types.UserTokenCreateResponse.from_dict,
        )

    def delete(
        self,
        user_id: str,
        token_id: str,
        request: Request | None = None,
    ) -> Response[types.UserTokenDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/user/{user_id}/token/{token_id}/delete",
            record=request or {},
            parse=types.UserTokenDeleteResponse.from_dict,
        )
