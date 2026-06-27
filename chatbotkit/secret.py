from __future__ import annotations

from typing import Any, Mapping

import httpx

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

    def mint(self, secret_id: str) -> Response[types.SecretMintResponse, Any]:
        """Mint a usable token from the secret (owner-only; oauth/jwt only)."""
        return self._client.client_fetch(
            f"/api/v1/secret/{secret_id}/mint",
            record={},
            parse=types.SecretMintResponse.from_dict,
        )

    async def proxy(
        self,
        secret_id: str,
        request: types.SecretProxyRequest | Request,
    ) -> httpx.Response:
        """Proxy a request through the secret, injected server-side.

        Returns the raw upstream response verbatim; a non-2xx status (including
        409 authorization_required) is returned, not raised.
        """
        return await self._client.request(
            f"/api/v1/secret/{secret_id}/proxy",
            method="POST",
            record=request,
            raw=True,
        )
