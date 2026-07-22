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
    abort_signal: asyncio.Event | None = None,
    **request: Any,
) -> AsyncIterator[dict[str, Any]]:
    """Complete one agent iteration and execute requested tools.

    When ``abort_signal`` is provided and becomes set, the stream stops being
    consumed at the next event boundary. Any tools already running are still
    awaited so their tasks do not leak.
    """

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
        if abort_signal is not None and abort_signal.is_set():
            break

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
    abort_signal: asyncio.Event | None = None,
    **request: Any,
) -> AsyncIterator[dict[str, Any]]:
    """Execute an agent loop until it exits or reaches the iteration limit.

    The agent runs until the model calls the built-in ``exit`` tool, the
    ``max_iterations`` limit is reached, the model finishes without pending
    tool calls, or ``abort_signal`` is set.

    Cancellation
    ------------
    Pass an :class:`asyncio.Event` as ``abort_signal`` to stop the loop from the
    outside (a timeout, a shutdown hook, a user pressing stop)::

        abort_signal = asyncio.Event()

        stream = execute(client=client, messages=messages, tools=tools,
                         abort_signal=abort_signal)

        abort_signal.set()  # stop the agent

    Setting it ends the current iteration at the next event boundary and exits
    with code ``1``. The built-in ``abort`` tool mirrors this: the model can call
    it to stop gracefully, and ``abort(hard=True)`` cancels the in-flight
    iteration immediately instead of letting it finish.

    Message injection
    -----------------
    In local mode, the ``messages`` list is used directly (not copied), so you
    can append new messages to it at any point while the agent is running. They
    are included in the context at the start of the next iteration::

        messages = [{"type": "user", "text": "Perform the task."}]

        stream = execute(client=client, messages=messages, tools=tools)

        # inject a user message or system notification mid-run:
        messages.append({"type": "user", "text": "Also handle edge case Y."})
        messages.append({"type": "context", "text": "System: disk usage at 90%."})

    The agent also appends its own ``bot`` responses to the same list as each
    iteration completes, so ``messages`` reflects the full conversation history
    and you do not need to accumulate it yourself.

    In remote mode, the conversation history is driven by the server through
    ``conversation_id``, so there is no local message list to mutate.
    """

    exit_result: dict[str, Any] | None = None

    # Per-iteration abort event a hard abort can set to cancel the in-flight
    # completion immediately. Recreated each iteration; the abort handler reads
    # whichever event is current when it fires.
    internal_abort: asyncio.Event | None = None

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

        if input.hard and internal_abort is not None:
            internal_abort.set()

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
        if abort_signal is not None and abort_signal.is_set():
            exit_result = {"code": 1, "message": "Task execution aborted"}
            break

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

        # Fresh per-iteration abort event, forwarded from the caller's signal so
        # an external abort mid-iteration also cancels the in-flight completion.
        internal_abort = asyncio.Event()
        abort_bridge = _start_abort_bridge(abort_signal, internal_abort)

        try:
            async for event in complete(
                client=client,
                conversation_id=conversation_id,
                tools=all_tools,
                abort_signal=internal_abort,
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
        finally:
            await _stop_abort_bridge(abort_bridge)

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


def _start_abort_bridge(
    source: asyncio.Event | None,
    target: asyncio.Event,
) -> asyncio.Task[None] | None:
    """Forward ``source`` into ``target`` so an external abort cancels the
    current iteration. Returns the watcher task to be stopped afterwards, or
    ``None`` when there is nothing to watch."""

    if source is None:
        return None

    if source.is_set():
        target.set()
        return None

    return asyncio.create_task(_forward_event(source, target))


async def _forward_event(source: asyncio.Event, target: asyncio.Event) -> None:
    await source.wait()
    target.set()


async def _stop_abort_bridge(task: asyncio.Task[None] | None) -> None:
    if task is None:
        return

    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        pass


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

1. **Plan First**: Use the 'plan' function to create a clear strategy before starting work
2. **Track Progress**: Regularly use the 'progress' function to update status and identify issues
3. **Use Tools**: Leverage available tools to accomplish each step of your plan
4. **Exit When Done**: Call the 'exit' function with code 0 when successful, or non-zero code if unable to complete
5. **Abort**: If the user asks you to stop, cancel, or abort, call the 'abort' function immediately. Use hard=true if processes are running that need to be killed right away.
6. **Be Autonomous**: Work through the task systematically without waiting for additional input
7. **Be Responsive**: If the user sends a new message while you are working, acknowledge it briefly and adjust your approach if needed. Always prioritize user input over your current plan.
""".strip()


def _exit_message(code: int, message: str | None) -> str:
    result = f"Task exiting with code {code}"

    if message:
        result = f"{result}: {message}"

    return result
