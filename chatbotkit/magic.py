from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class MagicClient:
    def __init__(self, client: Client) -> None:
        self._client = client
        self.prompt = MagicPromptClient(client)

    def generate(
        self,
        magic_id: str,
        request: types.MagicFromPromptGenerateRequest | Request,
    ) -> Response[types.MagicFromPromptGenerateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/magic/{magic_id}/generate",
            record=request,
            parse=types.MagicFromPromptGenerateResponse.from_dict,
        )


class MagicPromptClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.MagicPromptListParams | Request | None = None,
    ) -> Response[types.MagicPromptListResponse, types.MagicPromptListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/magic/prompt/list",
            query=request,
            parse=types.MagicPromptListResponse.from_dict,
            stream_parse=types.MagicPromptListStreamItem.from_dict,
        )
