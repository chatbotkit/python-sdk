from __future__ import annotations

from typing import Any, Mapping

from . import types
from ._transport import Client, Response

Request = Mapping[str, Any]


class TaskClient:
    def __init__(self, client: Client) -> None:
        self._client = client
        self.execution = TaskExecutionClient(client)

    def list(
        self,
        request: types.TaskListParams | Request | None = None,
    ) -> Response[types.TaskListResponse, types.TaskListStreamItem]:
        return self._client.client_fetch(
            "/api/v1/task/list",
            query=request,
            parse=types.TaskListResponse.from_dict,
            stream_parse=types.TaskListStreamItem.from_dict,
        )

    def fetch(self, task_id: str) -> Response[types.TaskFetchResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/task/{task_id}/fetch",
            parse=types.TaskFetchResponse.from_dict,
        )

    def create(
        self,
        request: types.TaskCreateRequest | Request,
    ) -> Response[types.TaskCreateResponse, Any]:
        return self._client.client_fetch(
            "/api/v1/task/create",
            record=request,
            parse=types.TaskCreateResponse.from_dict,
        )

    def update(
        self,
        task_id: str,
        request: types.TaskUpdateRequest | Request,
    ) -> Response[types.TaskUpdateResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/task/{task_id}/update",
            record=request,
            parse=types.TaskUpdateResponse.from_dict,
        )

    def delete(
        self,
        task_id: str,
        request: Request | None = None,
    ) -> Response[types.TaskDeleteResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/task/{task_id}/delete",
            record=request or {},
            parse=types.TaskDeleteResponse.from_dict,
        )

    def trigger(
        self,
        task_id: str,
        request: types.TaskTriggerRequest | Request | None = None,
    ) -> Response[types.TaskTriggerResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/task/{task_id}/trigger",
            record=request or {},
            parse=types.TaskTriggerResponse.from_dict,
        )

    def cancel(
        self,
        task_id: str,
        request: Request | None = None,
    ) -> Response[types.TaskCancelResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/task/{task_id}/cancel",
            record=request or {},
            parse=types.TaskCancelResponse.from_dict,
        )

    def export(
        self,
        request: types.TasksExportParams | Request | None = None,
    ) -> Response[types.TasksExportResponse, types.TasksExportStreamItem]:
        return self._client.client_fetch(
            "/api/v1/task/export",
            query=request,
            parse=types.TasksExportResponse.from_dict,
            stream_parse=types.TasksExportStreamItem.from_dict,
        )


class TaskExecutionClient:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        task_id: str,
        request: types.TaskExecutionListParams | Request | None = None,
    ) -> Response[
        types.TaskExecutionListResponse,
        types.TaskExecutionListStreamItem,
    ]:
        return self._client.client_fetch(
            f"/api/v1/task/{task_id}/execution/list",
            query=request,
            parse=types.TaskExecutionListResponse.from_dict,
            stream_parse=types.TaskExecutionListStreamItem.from_dict,
        )

    def cancel(
        self,
        task_id: str,
        execution_id: str,
        request: Request | None = None,
    ) -> Response[types.TaskExecutionCancelResponse, Any]:
        return self._client.client_fetch(
            f"/api/v1/task/{task_id}/execution/{execution_id}/cancel",
            record=request or {},
            parse=types.TaskExecutionCancelResponse.from_dict,
        )
