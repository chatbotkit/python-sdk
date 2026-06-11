from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Mapping

from pydantic import BaseModel

ToolHandler = Callable[[Any], Any | Awaitable[Any]]


@dataclass(frozen=True)
class Tool:
    description: str
    handler: ToolHandler
    input_model: type[BaseModel] | None = None
    parameters: Mapping[str, Any] | None = None
    call: Mapping[str, bool] | None = None

    def function_definition(self, name: str, channel: str) -> dict[str, Any]:
        definition: dict[str, Any] = {
            "name": name,
            "description": self.description,
            "parameters": self._parameters(),
            "result": {"channel": channel},
        }

        if self.call is not None:
            definition["call"] = dict(self.call)

        return definition

    async def run(self, args: Any) -> Any:
        parsed_args = self._parse_args(args)
        result = self.handler(parsed_args)

        if inspect.isawaitable(result):
            return await result

        return result

    def _parameters(self) -> dict[str, Any]:
        if self.parameters is not None:
            return dict(self.parameters)

        if self.input_model is None:
            return {"type": "object", "properties": {}}

        schema = self.input_model.model_json_schema()
        parameters: dict[str, Any] = {
            "type": "object",
            "properties": schema.get("properties", {}),
        }

        for key in ("required", "$defs", "definitions", "additionalProperties"):
            if key in schema:
                parameters[key] = schema[key]

        return parameters

    def _parse_args(self, args: Any) -> Any:
        if self.input_model is None:
            return args or {}

        return self.input_model.model_validate(args or {})


def normalize_tools(
    tools: Mapping[str, Tool | Mapping[str, Any]],
) -> dict[str, Tool]:
    normalized: dict[str, Tool] = {}

    for name, tool in tools.items():
        if isinstance(tool, Tool):
            normalized[name] = tool
            continue

        handler = tool.get("handler")

        if handler is None:
            raise TypeError(f"tool {name!r} must define a handler")

        normalized[name] = Tool(
            description=str(tool.get("description", "")),
            handler=handler,
            input_model=tool.get("input_model"),
            parameters=tool.get("parameters"),
            call=tool.get("call"),
        )

    return normalized
