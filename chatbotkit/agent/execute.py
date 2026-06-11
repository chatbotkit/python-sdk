from __future__ import annotations

import asyncio
import json
import secrets
import string
from typing import Any, AsyncIterator, Mapping

from pydantic import BaseModel, Field

from .tools import Tool, normalize_tools


class PlanInput(BaseModel):
    steps: list[str] = Field(
        description="Array of step descriptions in order of execution"
    )
    rationale: str | None = Field(
        default=None,
        description="Brief explanation of the plan approach",
    )


class ProgressInput(BaseModel):
    completed: list[str] | None = Field(
        default=None,
        description="Steps that have been completed",
    )
    current: str | None = Field(
        default=None,
        description="Current step being worked on",
    )
    blockers: list[str] | None = Field(
        default=None,
        description="Any issues preventing progress",
    )
    next_steps: list[str] | None = Field(
        default=None,
        alias="nextSteps",
        description="Next actions to take",
    )


class ExitInput(BaseModel):
    code: int = Field(
        ge=0,
        le=255,
        description="Exit status code. Use 0 for success and non-zero for failure.",
    )
    message: str | None = Field(
        default=None,
        description="Optional message explaining the exit reason",
    )


class AbortInput(BaseModel):
    reason: str | None = Field(
        default=None,
        description="Brief reason for aborting",
    )
    hard: bool | None = Field(
        default=None,
        description="Whether the current task should stop immediately",
    )


async def complete(
    *,
    client: Any,
    conversation_id: str | None = None,
    tools: Mapping[str, Tool | Mapping[str, Any]] | None = None,
    **request: Any,
) -> AsyncIterator[dict[str, Any]]:
    """Complete one agent iteration and execute requested tools."""

    channel_to_tool: dict[str, tuple[str, Tool]] = {}
    normalized_tools = normalize_tools(tools or {})

    functions: list[dict[str, Any]] = []

    for name, tool in normalized_tools.items():
        channel = _tool_channel(name)
        channel_to_tool[channel] = (name, tool)
        functions.append(tool.function_definition(name, channel))

    if functions:
        request["functions"] = functions

    request["limits"] = _with_iteration_limit(request.get("limits"))

    if conversation_id is None:
        response = client.client_fetch(
            "/api/v1/conversation/complete",
            record=request,
            parse=lambda data: data,
            stream_parse=lambda data: data,
        )
    else:
        response = client.client_fetch(
            f"/api/v1/conversation/{conversation_id}/complete",
            endpoint="/api/v1/conversation/{conversationId}/complete",
            record=request,
            parse=lambda data: data,
            stream_parse=lambda data: data,
        )

    tool_events: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
    running_tools: list[asyncio.Task[None]] = []

    async for event in response.stream():
        for queued_event in _drain_tool_events(tool_events):
            yield queued_event

        tool_call = _extract_tool_call(event)

        if tool_call is not None:
            channel, args = tool_call
            tool_info = channel_to_tool.get(channel)

            if tool_info is not None:
                name, tool = tool_info

                yield {
                    "type": "toolCallStart",
                    "data": {"name": name, "args": args},
                }

                running_tools.append(
                    asyncio.create_task(
                        _run_tool(client, channel, name, tool, args, tool_events)
                    )
                )

        yield event

    for queued_event in _drain_tool_events(tool_events):
        yield queued_event

    if running_tools:
        await asyncio.gather(*running_tools, return_exceptions=True)

        for queued_event in _drain_tool_events(tool_events):
            yield queued_event


async def execute(
    *,
    client: Any,
    conversation_id: str | None = None,
    tools: Mapping[str, Tool | Mapping[str, Any]] | None = None,
    max_iterations: int = 100,
    **request: Any,
) -> AsyncIterator[dict[str, Any]]:
    """Execute an agent loop until it exits or reaches the iteration limit."""

    exit_result: dict[str, Any] | None = None

    async def plan(input: PlanInput) -> dict[str, Any]:
        message = f"Plan created with {len(input.steps)} steps"

        if input.rationale:
            message = f"{message}: {input.rationale}"

        return {"success": True, "message": message}

    async def progress(input: ProgressInput) -> dict[str, Any]:
        return {
            "success": True,
            "message": "Progress updated",
            **input.model_dump(by_alias=True, exclude_none=True),
        }

    async def exit(input: ExitInput) -> dict[str, Any]:
        nonlocal exit_result

        exit_result = input.model_dump(exclude_none=True)

        return {
            "success": True,
            "message": _exit_message(input.code, input.message),
        }

    async def abort(input: AbortInput) -> dict[str, Any]:
        nonlocal exit_result

        reason = input.reason or "aborted by user request"
        exit_result = {"code": 1, "message": reason}

        return {
            "success": True,
            "message": f"Task aborted: {reason}",
        }

    system_tools = {
        "plan": Tool(
            description=(
                "Create or update a plan for approaching the task. Break down "
                "the task into clear, actionable steps."
            ),
            input_model=PlanInput,
            handler=plan,
        ),
        "progress": Tool(
            description=(
                "Update progress on the current task. Use this to track "
                "completed steps, current status, and blockers."
            ),
            input_model=ProgressInput,
            handler=progress,
        ),
        "exit": Tool(
            description=(
                "Exit task execution with a status code and optional message. "
                "Use 0 for success and non-zero for failure."
            ),
            input_model=ExitInput,
            handler=exit,
        ),
        "abort": Tool(
            description=(
                "Abort the current task when the user asks to stop, cancel, or "
                "abort the work."
            ),
            input_model=AbortInput,
            handler=abort,
        ),
    }

    all_tools = {**normalize_tools(tools or {}), **system_tools}
    user_extensions = request.get("extensions") or {}

    if not isinstance(user_extensions, Mapping):
        raise TypeError("extensions must be a mapping when passed to execute")

    system_instruction = _system_instruction(user_extensions.get("backstory"))

    iteration = 0

    while iteration < max_iterations and exit_result is None:
        iteration += 1

        yield {"type": "iteration", "data": {"iteration": iteration}}

        last_end_reason: str | None = None
        iteration_request = {
            **request,
            "extensions": {
                **user_extensions,
                "backstory": system_instruction,
            },
        }

        async for event in complete(
            client=client,
            conversation_id=conversation_id,
            tools=all_tools,
            **iteration_request,
        ):
            if event.get("type") == "message" and isinstance(
                request.get("messages"), list
            ):
                data = event.get("data")

                if isinstance(data, Mapping):
                    request["messages"].append(dict(data))

            if event.get("type") == "result":
                reason = _result_end_reason(event)

                if reason is not None:
                    last_end_reason = reason

            yield event

        if exit_result is not None:
            break

        if last_end_reason in {"stop", "abort"}:
            exit_result = {"code": 0}
            break

    if exit_result is None:
        exit_result = {
            "code": 1,
            "message": f"Task did not complete within {max_iterations} iterations",
        }

    yield {"type": "exit", "data": exit_result}


async def _run_tool(
    client: Any,
    channel: str,
    name: str,
    tool: Tool,
    args: Any,
    events: asyncio.Queue[dict[str, Any]],
) -> None:
    try:
        result = await tool.run(args)
    except Exception as error:
        error_message = str(error) or type(error).__name__
        await events.put(
            {
                "type": "toolCallError",
                "data": {"name": name, "error": error_message},
            }
        )
        await client.channel.publish(channel, {"message": {"error": error_message}})
    else:
        await events.put(
            {
                "type": "toolCallEnd",
                "data": {"name": name, "result": result},
            }
        )
        await client.channel.publish(channel, {"message": {"data": result}})


def _tool_channel(name: str) -> str:
    alphabet = string.ascii_lowercase + string.digits
    suffix = "".join(secrets.choice(alphabet) for _ in range(12))

    return f"{name}_{suffix}"


def _with_iteration_limit(limits: Any) -> dict[str, Any]:
    if limits is None:
        return {"iterations": 1}

    if not isinstance(limits, Mapping):
        raise TypeError("limits must be a mapping when passed to complete")

    return {**limits, "iterations": 1}


def _extract_tool_call(event: dict[str, Any]) -> tuple[str, Any] | None:
    if event.get("type") != "waitForChannelMessageBegin":
        return None

    data = event.get("data")

    if not isinstance(data, Mapping):
        return None

    channel = data.get("channel")
    function = data.get("function")

    if not isinstance(channel, str) or not isinstance(function, Mapping):
        return None

    return channel, _decode_args(function.get("args", {}))


def _decode_args(args: Any) -> Any:
    if not isinstance(args, str):
        return args

    try:
        return json.loads(args)
    except json.JSONDecodeError:
        return args


def _drain_tool_events(
    events: asyncio.Queue[dict[str, Any]],
) -> list[dict[str, Any]]:
    drained: list[dict[str, Any]] = []

    while True:
        try:
            drained.append(events.get_nowait())
        except asyncio.QueueEmpty:
            return drained


def _result_end_reason(event: dict[str, Any]) -> str | None:
    data = event.get("data")

    if not isinstance(data, Mapping):
        return None

    end = data.get("end")

    if not isinstance(end, Mapping):
        return None

    reason = end.get("reason")

    return reason if isinstance(reason, str) else None


def _system_instruction(backstory: Any) -> str:
    prefix = backstory if isinstance(backstory, str) else ""

    return f"""
{prefix}

# Task Execution Guidelines

The goal is to complete the assigned task efficiently and effectively. Follow these guidelines:

1. Plan first with the plan tool.
2. Track progress with the progress tool.
3. Use available tools to accomplish each step.
4. Call exit with code 0 when successful, or a non-zero code if unable to complete.
5. Call abort if the user asks you to stop, cancel, or abort the work.
6. Work autonomously and adjust when new user input changes the task.
""".strip()


def _exit_message(code: int, message: str | None) -> str:
    result = f"Task exiting with code {code}"

    if message:
        result = f"{result}: {message}"

    return result
