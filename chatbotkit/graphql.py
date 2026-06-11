from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class GraphqlClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def call(
        self,
        request: types.GraphqlRequest | Request,
    ) -> Response[types.GraphqlResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/graphql",
            record=request,
            parse=types.GraphqlResponse.from_dict,
        )
