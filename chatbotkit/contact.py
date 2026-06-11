from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class ContactClient:
    def __init__(self, client: Client) -> None:
        self._client = client
        self.conversation = ContactConversationClient(client)
        self.secret = ContactSecretClient(client)
        self.space = ContactSpaceClient(client)
        self.task = ContactTaskClient(client)

    def list(
        self,
        request: types.ContactListParams | Request | None = None,
    ) -> Response[types.ContactListResponse, types.ContactListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/contact/list",
            query=request,
            parse=types.ContactListResponse.from_dict,
            stream_parse=types.ContactListStreamItem.from_dict,
        )

    def fetch(self, contact_id: str) -> Response[types.ContactFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/contact/{contact_id}/fetch",
            parse=types.ContactFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.ContactCreateRequest | Request,
    ) -> Response[types.ContactCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/contact/create",
            record=request,
            parse=types.ContactCreateResponse.from_dict,
        )

    def ensure(
        self,
        request: types.ContactEnsureRequest | Request,
    ) -> Response[types.ContactEnsureResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/contact/ensure",
            record=request,
            parse=types.ContactEnsureResponse.from_dict,
        )

    def update(
        self,
        contact_id: str,
        request: types.ContactUpdateRequest | Request,
    ) -> Response[types.ContactUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/contact/{contact_id}/update",
            record=request,
            parse=types.ContactUpdateResponse.from_dict,
        )

    def delete(
        self,
        contact_id: str,
        request: Request | None = None,
    ) -> Response[types.ContactDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/contact/{contact_id}/delete",
            record=request or {},
            parse=types.ContactDeleteResponse.from_dict,
        )


class ContactConversationClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        contact_id: str,
        request: types.ContactConversationListParams | Request | None = None,
    ) -> Response[
        types.ContactConversationListResponse,
        types.ContactConversationListStreamItem,
    ]:
        return self._client.client_fetch(
            f"/api/v1/contact/{contact_id}/conversation/list",
            query=request,
            parse=types.ContactConversationListResponse.from_dict,
            stream_parse=types.ContactConversationListStreamItem.from_dict,
        )


class ContactSecretClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        contact_id: str,
        request: types.ContactSecretListParams | Request | None = None,
    ) -> Response[
        types.ContactSecretListResponse,
        types.ContactSecretListStreamItem,
    ]:
        return self._client.client_fetch(
            f"/api/v1/contact/{contact_id}/secret/list",
            query=request,
            parse=types.ContactSecretListResponse.from_dict,
            stream_parse=types.ContactSecretListStreamItem.from_dict,
        )


class ContactSpaceClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        contact_id: str,
        request: types.ContactSpaceListParams | Request | None = None,
    ) -> Response[
        types.ContactSpaceListResponse,
        types.ContactSpaceListStreamItem,
    ]:
        return self._client.client_fetch(
            f"/api/v1/contact/{contact_id}/space/list",
            query=request,
            parse=types.ContactSpaceListResponse.from_dict,
            stream_parse=types.ContactSpaceListStreamItem.from_dict,
        )


class ContactTaskClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        contact_id: str,
        request: types.ContactTaskListParams | Request | None = None,
    ) -> Response[
        types.ContactTaskListResponse,
        types.ContactTaskListStreamItem,
    ]:
        return self._client.client_fetch(
            f"/api/v1/contact/{contact_id}/task/list",
            query=request,
            parse=types.ContactTaskListResponse.from_dict,
            stream_parse=types.ContactTaskListStreamItem.from_dict,
        )
