from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class PlatformClient:
    def __init__(self, client: Client) -> None:
        self._client = client
        self.ability = PlatformAbilityClient(client)
        self.action = PlatformActionClient(client)
        self.doc = PlatformDocClient(client)
        self.example = PlatformExampleClient(client)
        self.manual = PlatformManualClient(client)
        self.model = PlatformModelClient(client)
        self.report = PlatformReportClient(client)
        self.secret = PlatformSecretClient(client)
        self.tutorial = PlatformTutorialClient(client)


class PlatformAbilityClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.PlatformAbilityListParams | Request | None = None,
    ) -> Response[
        types.PlatformAbilityListResponse,
        types.PlatformAbilityListStreamItem,
    ]:
        return self._client.client_fetch(
            "/api/v1/platform/ability/list",
            query=request,
            parse=types.PlatformAbilityListResponse.from_dict,
            stream_parse=types.PlatformAbilityListStreamItem.from_dict,
        )

    def search(
        self,
        request: types.PlatformAbilitiesSearchRequest | Request,
    ) -> Response[types.PlatformAbilitiesSearchResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/platform/ability/search",
            record=request,
            parse=types.PlatformAbilitiesSearchResponse.from_dict,
        )


class PlatformActionClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.PlatformActionListParams | Request | None = None,
    ) -> Response[
        types.PlatformActionListResponse,
        types.PlatformActionListStreamItem,
    ]:
        return self._client.client_fetch(
            "/api/v1/platform/action/list",
            query=request,
            parse=types.PlatformActionListResponse.from_dict,
            stream_parse=types.PlatformActionListStreamItem.from_dict,
        )


class PlatformDocClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.PlatformDocListParams | Request | None = None,
    ) -> Response[types.PlatformDocListResponse, types.PlatformDocListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/platform/doc/list",
            query=request,
            parse=types.PlatformDocListResponse.from_dict,
            stream_parse=types.PlatformDocListStreamItem.from_dict,
        )

    def search(
        self,
        request: types.PlatformDocsSearchRequest | Request,
    ) -> Response[types.PlatformDocsSearchResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/platform/doc/search",
            record=request,
            parse=types.PlatformDocsSearchResponse.from_dict,
        )

    def fetch(self, doc_id: str) -> Response[types.PlatformDocFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/platform/doc/{doc_id}/fetch",
            parse=types.PlatformDocFetchResponse.from_dict,
        )


class PlatformExampleClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.PlatformExampleListParams | Request | None = None,
    ) -> Response[
        types.PlatformExampleListResponse,
        types.PlatformExampleListStreamItem,
    ]:
        return self._client.client_fetch(
            "/api/v1/platform/example/list",
            query=request,
            parse=types.PlatformExampleListResponse.from_dict,
            stream_parse=types.PlatformExampleListStreamItem.from_dict,
        )

    def search(
        self,
        request: types.PlatformExamplesSearchRequest | Request,
    ) -> Response[types.PlatformExamplesSearchResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/platform/example/search",
            record=request,
            parse=types.PlatformExamplesSearchResponse.from_dict,
        )

    def fetch(self, example_id: str) -> Response[types.PlatformExampleFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/platform/example/{example_id}/fetch",
            parse=types.PlatformExampleFetchResponse.from_dict,
        )


class PlatformManualClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.PlatformManualListParams | Request | None = None,
    ) -> Response[
        types.PlatformManualListResponse,
        types.PlatformManualListStreamItem,
    ]:
        return self._client.client_fetch(
            "/api/v1/platform/manual/list",
            query=request,
            parse=types.PlatformManualListResponse.from_dict,
            stream_parse=types.PlatformManualListStreamItem.from_dict,
        )

    def search(
        self,
        request: types.PlatformManualsSearchRequest | Request,
    ) -> Response[types.PlatformManualsSearchResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/platform/manual/search",
            record=request,
            parse=types.PlatformManualsSearchResponse.from_dict,
        )

    def fetch(self, manual_id: str) -> Response[types.PlatformManualFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/platform/manual/{manual_id}/fetch",
            parse=types.PlatformManualFetchResponse.from_dict,
        )


class PlatformModelClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.PlatformModelListParams | Request | None = None,
    ) -> Response[
        types.PlatformModelListResponse,
        types.PlatformModelListStreamItem,
    ]:
        return self._client.client_fetch(
            "/api/v1/platform/model/list",
            query=request,
            parse=types.PlatformModelListResponse.from_dict,
            stream_parse=types.PlatformModelListStreamItem.from_dict,
        )


class PlatformReportClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.PlatformReportListParams | Request | None = None,
    ) -> Response[
        types.PlatformReportListResponse,
        types.PlatformReportListStreamItem,
    ]:
        return self._client.client_fetch(
            "/api/v1/platform/report/list",
            query=request,
            parse=types.PlatformReportListResponse.from_dict,
            stream_parse=types.PlatformReportListStreamItem.from_dict,
        )


class PlatformSecretClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.PlatformSecretListParams | Request | None = None,
    ) -> Response[
        types.PlatformSecretListResponse,
        types.PlatformSecretListStreamItem,
    ]:
        return self._client.client_fetch(
            "/api/v1/platform/secret/list",
            query=request,
            parse=types.PlatformSecretListResponse.from_dict,
            stream_parse=types.PlatformSecretListStreamItem.from_dict,
        )

    def search(
        self,
        request: types.PlatformSecretsSearchRequest | Request,
    ) -> Response[types.PlatformSecretsSearchResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/platform/secret/search",
            record=request,
            parse=types.PlatformSecretsSearchResponse.from_dict,
        )


class PlatformTutorialClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        request: types.PlatformTutorialListParams | Request | None = None,
    ) -> Response[
        types.PlatformTutorialListResponse,
        types.PlatformTutorialListStreamItem,
    ]:
        return self._client.client_fetch(
            "/api/v1/platform/tutorial/list",
            query=request,
            parse=types.PlatformTutorialListResponse.from_dict,
            stream_parse=types.PlatformTutorialListStreamItem.from_dict,
        )

    def search(
        self,
        request: types.PlatformTutorialsSearchRequest | Request,
    ) -> Response[types.PlatformTutorialsSearchResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/platform/tutorial/search",
            record=request,
            parse=types.PlatformTutorialsSearchResponse.from_dict,
        )

    def fetch(self, tutorial_id: str) -> Response[types.PlatformTutorialFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/platform/tutorial/{tutorial_id}/fetch",
            parse=types.PlatformTutorialFetchResponse.from_dict,
        )
