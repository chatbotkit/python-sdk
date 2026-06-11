from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class ChannelClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def publish(
        self,
        channel: str,
        request: types.ChannelMessagePublishRequest | Request,
    ) -> Response[types.ChannelMessagePublishResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/channel/{channel}/publish",
            record=request,
            parse=types.ChannelMessagePublishResponse.from_dict,
        )

    def subscribe(
        self,
        channel: str,
        request: types.ChannelMessagesSubscribeRequest | Request | None = None,
    ) -> Response[Any, types.ChannelMessagesSubscribeStreamItem]:
        return self._client.client_fetch(
            f"/api/v1/channel/{channel}/subscribe",
            record=request or {},
            stream_parse=types.ChannelMessagesSubscribeStreamItem.from_dict,
        )
