from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class SkillsetClient:
    def __init__(self, client: Client) -> None:
        self._client = client
        self.ability = SkillsetAbilityClient(client)

    def list(
        self,
        request: types.SkillsetListParams | Request | None = None,
    ) -> Response[types.SkillsetListResponse, types.SkillsetListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/skillset/list",
            query=request,
            parse=types.SkillsetListResponse.from_dict,
            stream_parse=types.SkillsetListStreamItem.from_dict,
        )

    def fetch(self, skillset_id: str) -> Response[types.SkillsetFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/skillset/{skillset_id}/fetch",
            parse=types.SkillsetFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.SkillsetCreateRequest | Request,
    ) -> Response[types.SkillsetCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/skillset/create",
            record=request,
            parse=types.SkillsetCreateResponse.from_dict,
        )

    def update(
        self,
        skillset_id: str,
        request: types.SkillsetUpdateRequest | Request,
    ) -> Response[types.SkillsetUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/skillset/{skillset_id}/update",
            record=request,
            parse=types.SkillsetUpdateResponse.from_dict,
        )

    def delete(
        self,
        skillset_id: str,
        request: Request | None = None,
    ) -> Response[types.SkillsetDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/skillset/{skillset_id}/delete",
            record=request or {},
            parse=types.SkillsetDeleteResponse.from_dict,
        )


class SkillsetAbilityClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        skillset_id: str,
        request: types.SkillsetAbilityListParams | Request | None = None,
    ) -> Response[
        types.SkillsetAbilityListResponse,
        types.SkillsetAbilityListStreamItem,
    ]:
        return self._client.client_fetch(
            f"/api/v1/skillset/{skillset_id}/ability/list",
            query=request,
            parse=types.SkillsetAbilityListResponse.from_dict,
            stream_parse=types.SkillsetAbilityListStreamItem.from_dict,
        )

    def fetch(
        self,
        skillset_id: str,
        ability_id: str,
    ) -> Response[types.SkillsetAbilityFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/skillset/{skillset_id}/ability/{ability_id}/fetch",
            parse=types.SkillsetAbilityFetchResponse.from_dict,
        )

    def create(
        self,
        skillset_id: str,
        request: types.SkillsetAbilityCreateRequest | Request,
    ) -> Response[types.SkillsetAbilityCreateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/skillset/{skillset_id}/ability/create",
            record=request,
            parse=types.SkillsetAbilityCreateResponse.from_dict,
        )

    def update(
        self,
        skillset_id: str,
        ability_id: str,
        request: types.SkillsetAbilityUpdateRequest | Request,
    ) -> Response[types.SkillsetAbilityUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/skillset/{skillset_id}/ability/{ability_id}/update",
            record=request,
            parse=types.SkillsetAbilityUpdateResponse.from_dict,
        )

    def delete(
        self,
        skillset_id: str,
        ability_id: str,
        request: Request | None = None,
    ) -> Response[types.SkillsetAbilityDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/skillset/{skillset_id}/ability/{ability_id}/delete",
            record=request or {},
            parse=types.SkillsetAbilityDeleteResponse.from_dict,
        )

    def export(
        self,
        skillset_id: str,
        request: types.SkillsetAbilitiesExportParams | Request | None = None,
    ) -> Response[
        types.SkillsetAbilitiesExportResponse,
        types.SkillsetAbilitiesExportStreamItem,
    ]:
        return self._client.client_fetch(
            f"/api/v1/skillset/{skillset_id}/ability/export",
            query=request,
            parse=types.SkillsetAbilitiesExportResponse.from_dict,
            stream_parse=types.SkillsetAbilitiesExportStreamItem.from_dict,
        )
