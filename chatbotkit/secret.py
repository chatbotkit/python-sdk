from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class SecretClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.SecretListParams | Request | None = None,
    ) -> Response[types.SecretListResponse, types.SecretListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/secret/list",
            query=request,
            parse=types.SecretListResponse.from_dict,
            stream_parse=types.SecretListStreamItem.from_dict,
        )

    def fetch(self, secret_id: str) -> Response[types.SecretFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/secret/{secret_id}/fetch",
            parse=types.SecretFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.SecretCreateRequest | Request,
    ) -> Response[types.SecretCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/secret/create",
            record=request,
            parse=types.SecretCreateResponse.from_dict,
        )

    def update(
        self,
        secret_id: str,
        request: types.SecretUpdateRequest | Request,
    ) -> Response[types.SecretUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/secret/{secret_id}/update",
            record=request,
            parse=types.SecretUpdateResponse.from_dict,
        )

    def delete(
        self,
        secret_id: str,
        request: Request | None = None,
    ) -> Response[types.SecretDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/secret/{secret_id}/delete",
            record=request or {},
            parse=types.SecretDeleteResponse.from_dict,
        )
