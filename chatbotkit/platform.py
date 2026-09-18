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
        self.example = PlatformExampleClient(client)
        self.model = PlatformModelClient(client)
        self.report = PlatformReportClient(client)
        self.secret = PlatformSecretClient(client)


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
