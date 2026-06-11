from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class ConversationClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.ConversationListParams | Request | None = None,
    ) -> Response[types.ConversationListResponse, types.ConversationListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/conversation/list",
            query=request,
            parse=types.ConversationListResponse.from_dict,
            stream_parse=types.ConversationListStreamItem.from_dict,
        )

    def fetch(self, conversation_id: str) -> Response[types.ConversationFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/conversation/{conversation_id}/fetch",
            endpoint="/api/v1/conversation/{conversationId}/fetch",
            parse=types.ConversationFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.ConversationCreateRequest | Request,
    ) -> Response[types.ConversationCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/conversation/create",
            record=request,
            parse=types.ConversationCreateResponse.from_dict,
        )

    def update(
        self,
        conversation_id: str,
        request: types.ConversationUpdateRequest | Request,
    ) -> Response[types.ConversationUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/conversation/{conversation_id}/update",
            endpoint="/api/v1/conversation/{conversationId}/update",
            record=request,
            parse=types.ConversationUpdateResponse.from_dict,
        )

    def delete(
        self,
        conversation_id: str,
        request: Request | None = None,
    ) -> Response[types.ConversationDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/conversation/{conversation_id}/delete",
            endpoint="/api/v1/conversation/{conversationId}/delete",
            record=request or {},
            parse=types.ConversationDeleteResponse.from_dict,
        )

    def complete(
        self,
        conversation_id: str | None,
        request: types.ConversationCompleteRequest
        | types.ConversationMessageCompleteRequest
        | Request,
    ) -> Response[
        types.ConversationCompleteResponse | types.ConversationMessageCompleteResponse,
        types.ConversationCompleteStreamItem
        | types.ConversationMessageCompleteStreamItem,
    ]:
        if conversation_id is None:
            return self._client.client_fetch(
                "/api/v1/conversation/complete",
                record=request,
                parse=types.ConversationCompleteResponse.from_dict,
                stream_parse=types.ConversationCompleteStreamItem.from_dict,
            )

        return self._client.client_fetch(
            f"/api/v1/conversation/{conversation_id}/complete",
            endpoint="/api/v1/conversation/{conversationId}/complete",
            record=request,
            parse=types.ConversationMessageCompleteResponse.from_dict,
            stream_parse=types.ConversationMessageCompleteStreamItem.from_dict,
        )

    def dispatch(
        self,
        conversation_id: str | None,
        request: types.ConversationDispatchRequest
        | types.StatefulConversationDispatchRequest
        | Request,
    ) -> Response[
        types.ConversationDispatchResponse | types.StatefulConversationDispatchResponse,
        Any,
    ]:
        if conversation_id is None:
            return self._client.client_fetch(
                "/api/v1/conversation/dispatch",
                record=request,
                parse=types.ConversationDispatchResponse.from_dict,
            )

        return self._client.client_fetch(
            f"/api/v1/conversation/{conversation_id}/dispatch",
            endpoint="/api/v1/conversation/{conversationId}/dispatch",
            record=request,
            parse=types.StatefulConversationDispatchResponse.from_dict,
        )

    def send(
        self,
        conversation_id: str,
        request: types.ConversationMessageSendRequest | Request,
    ) -> Response[
        types.ConversationMessageSendResponse,
        types.ConversationMessageSendStreamItem,
    ]:
        return self._client.client_fetch(
            f"/api/v1/conversation/{conversation_id}/send",
            endpoint="/api/v1/conversation/{conversationId}/send",
            record=request,
            parse=types.ConversationMessageSendResponse.from_dict,
            stream_parse=types.ConversationMessageSendStreamItem.from_dict,
        )

    def receive(
        self,
        conversation_id: str,
        request: types.ConversationMessageReceiveRequest | Request,
    ) -> Response[
        types.ConversationMessageReceiveResponse,
        types.ConversationMessageReceiveStreamItem,
    ]:
        return self._client.client_fetch(
            f"/api/v1/conversation/{conversation_id}/receive",
            endpoint="/api/v1/conversation/{conversationId}/receive",
            record=request,
            parse=types.ConversationMessageReceiveResponse.from_dict,
            stream_parse=types.ConversationMessageReceiveStreamItem.from_dict,
        )

    def upvote(
        self,
        conversation_id: str,
        request: types.ConversationUpvoteRequest | Request,
    ) -> Response[types.ConversationUpvoteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/conversation/{conversation_id}/upvote",
            endpoint="/api/v1/conversation/{conversationId}/upvote",
            record=request,
            parse=types.ConversationUpvoteResponse.from_dict,
        )

    def downvote(
        self,
        conversation_id: str,
        request: types.ConversationDownvoteRequest | Request,
    ) -> Response[types.ConversationDownvoteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/conversation/{conversation_id}/downvote",
            endpoint="/api/v1/conversation/{conversationId}/downvote",
            record=request,
            parse=types.ConversationDownvoteResponse.from_dict,
        )
