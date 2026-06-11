from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class DatasetClient:
    def __init__(self, client: Client) -> None:
        self._client = client
        self.record = DatasetRecordClient(client)

    def list(
        self,
        request: types.DatasetListParams | Request | None = None,
    ) -> Response[types.DatasetListResponse, types.DatasetListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/dataset/list",
            query=request,
            parse=types.DatasetListResponse.from_dict,
            stream_parse=types.DatasetListStreamItem.from_dict,
        )

    def fetch(self, dataset_id: str) -> Response[types.DatasetFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/dataset/{dataset_id}/fetch",
            parse=types.DatasetFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.DatasetCreateRequest | Request,
    ) -> Response[types.DatasetCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/dataset/create",
            record=request,
            parse=types.DatasetCreateResponse.from_dict,
        )

    def update(
        self,
        dataset_id: str,
        request: types.DatasetUpdateRequest | Request,
    ) -> Response[types.DatasetUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/dataset/{dataset_id}/update",
            record=request,
            parse=types.DatasetUpdateResponse.from_dict,
        )

    def delete(
        self,
        dataset_id: str,
        request: Request | None = None,
    ) -> Response[types.DatasetDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/dataset/{dataset_id}/delete",
            record=request or {},
            parse=types.DatasetDeleteResponse.from_dict,
        )

    def search(
        self,
        dataset_id: str,
        request: types.DatasetSearchRequest | Request,
    ) -> Response[types.DatasetSearchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/dataset/{dataset_id}/search",
            record=request,
            parse=types.DatasetSearchResponse.from_dict,
        )


class DatasetRecordClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        dataset_id: str,
        request: types.DatasetRecordListParams | Request | None = None,
    ) -> Response[types.DatasetRecordListResponse, types.DatasetRecordListStreamItem]:
        return self._client.client_fetch(
            f"/api/v1/dataset/{dataset_id}/record/list",
            query=request,
            parse=types.DatasetRecordListResponse.from_dict,
            stream_parse=types.DatasetRecordListStreamItem.from_dict,
        )

    def fetch(
        self,
        dataset_id: str,
        record_id: str,
    ) -> Response[types.DatasetRecordFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/dataset/{dataset_id}/record/{record_id}/fetch",
            parse=types.DatasetRecordFetchResponse.from_dict,
        )

    def create(
        self,
        dataset_id: str,
        request: types.DatasetRecordCreateRequest | Request,
    ) -> Response[types.DatasetRecordCreateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/dataset/{dataset_id}/record/create",
            record=request,
            parse=types.DatasetRecordCreateResponse.from_dict,
        )

    def update(
        self,
        dataset_id: str,
        record_id: str,
        request: types.DatasetRecordUpdateRequest | Request,
    ) -> Response[types.DatasetRecordUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/dataset/{dataset_id}/record/{record_id}/update",
            record=request,
            parse=types.DatasetRecordUpdateResponse.from_dict,
        )

    def delete(
        self,
        dataset_id: str,
        record_id: str,
        request: Request | None = None,
    ) -> Response[types.DatasetRecordDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/dataset/{dataset_id}/record/{record_id}/delete",
            record=request or {},
            parse=types.DatasetRecordDeleteResponse.from_dict,
        )

    def export(
        self,
        dataset_id: str,
        request: types.DatasetRecordsExportParams | Request | None = None,
    ) -> Response[
        types.DatasetRecordsExportResponse,
        types.DatasetRecordsExportStreamItem,
    ]:
        return self._client.client_fetch(
            f"/api/v1/dataset/{dataset_id}/record/export",
            query=request,
            parse=types.DatasetRecordsExportResponse.from_dict,
            stream_parse=types.DatasetRecordsExportStreamItem.from_dict,
        )
