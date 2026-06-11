from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class PolicyClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.PolicyListParams | Request | None = None,
    ) -> Response[types.PolicyListResponse, types.PolicyListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/policy/list",
            query=request,
            parse=types.PolicyListResponse.from_dict,
            stream_parse=types.PolicyListStreamItem.from_dict,
        )

    def fetch(self, policy_id: str) -> Response[types.PolicyFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/policy/{policy_id}/fetch",
            parse=types.PolicyFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.PolicyCreateRequest | Request,
    ) -> Response[types.PolicyCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/policy/create",
            record=request,
            parse=types.PolicyCreateResponse.from_dict,
        )

    def update(
        self,
        policy_id: str,
        request: types.PolicyUpdateRequest | Request,
    ) -> Response[types.PolicyUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/policy/{policy_id}/update",
            record=request,
            parse=types.PolicyUpdateResponse.from_dict,
        )

    def delete(
        self,
        policy_id: str,
        request: Request | None = None,
    ) -> Response[types.PolicyDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/policy/{policy_id}/delete",
            record=request or {},
            parse=types.PolicyDeleteResponse.from_dict,
        )
