from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class EventClient:
    def __init__(self, client: Client) -> None:
        self._client = client
        self.log = EventLogClient(client)


class EventLogClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.EventLogListParams | Request | None = None,
    ) -> Response[types.EventLogListResponse, types.EventLogListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/event/log/list",
            query=request,
            parse=types.EventLogListResponse.from_dict,
            stream_parse=types.EventLogListStreamItem.from_dict,
        )

    def export(
        self,
        request: types.EventLogsExportParams | Request | None = None,
    ) -> Response[types.EventLogsExportResponse, types.EventLogsExportStreamItem]:
        return self._client.client_fetch(
            "/api/v1/event/log/export",
            query=request,
            parse=types.EventLogsExportResponse.from_dict,
            stream_parse=types.EventLogsExportStreamItem.from_dict,
        )
