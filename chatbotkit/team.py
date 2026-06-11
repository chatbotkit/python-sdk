from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class TeamClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.TeamListParams | Request | None = None,
    ) -> Response[types.TeamListResponse, types.TeamListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/team/list",
            query=request,
            parse=types.TeamListResponse.from_dict,
            stream_parse=types.TeamListStreamItem.from_dict,
        )
