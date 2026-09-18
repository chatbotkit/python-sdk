from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class DecisionClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def create(
        self,
        request: types.DecisionCreateRequest | Request,
    ) -> Response[types.DecisionCreateResponse, Any]:
        """Answers typed questions about a state.

        Pass a mapping for choice questions: the generated ``Question`` type
        cannot hold the named options of their ``criteria``.
        """
        return self._client.client_fetch(
            "/api/v1/decision/create",
            record=request,
            parse=types.DecisionCreateResponse.from_dict,
        )
