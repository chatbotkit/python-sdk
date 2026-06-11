from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class BotClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.BotListParams | Request | None = None,
    ) -> Response[types.BotListResponse, types.BotListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/bot/list",
            query=request,
            parse=types.BotListResponse.from_dict,
            stream_parse=types.BotListStreamItem.from_dict,
        )

    def fetch(self, bot_id: str) -> Response[types.BotFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/bot/{bot_id}/fetch",
            parse=types.BotFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.BotCreateRequest | Request,
    ) -> Response[types.BotCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/bot/create",
            record=request,
            parse=types.BotCreateResponse.from_dict,
        )

    def update(
        self,
        bot_id: str,
        request: types.BotUpdateRequest | Request,
    ) -> Response[types.BotUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/bot/{bot_id}/update",
            record=request,
            parse=types.BotUpdateResponse.from_dict,
        )

    def delete(
        self,
        bot_id: str,
        request: Request | None = None,
    ) -> Response[types.BotDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/bot/{bot_id}/delete",
            record=request or {},
            parse=types.BotDeleteResponse.from_dict,
        )

    def upvote(
        self,
        bot_id: str,
        request: types.BotUpvoteRequest | Request,
    ) -> Response[types.BotUpvoteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/bot/{bot_id}/upvote",
            record=request,
            parse=types.BotUpvoteResponse.from_dict,
        )

    def downvote(
        self,
        bot_id: str,
        request: types.BotDownvoteRequest | Request,
    ) -> Response[types.BotDownvoteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/bot/{bot_id}/downvote",
            record=request,
            parse=types.BotDownvoteResponse.from_dict,
        )
