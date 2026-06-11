from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class AgentDefinition:
    name: str | None = None
    description: str | None = None
    backstory: str | None = None
    model: str | None = None
    bot_id: str | None = None
    skillset_id: str | None = None
    dataset_id: str | None = None


def load_agent(file_path: str, roots: Iterable[str] | None = None) -> AgentDefinition:
    """Load an agent definition from a markdown file."""

    resolved_path = _resolve_file(file_path, roots)
    content = resolved_path.read_text(encoding="utf-8")
    front_matter, body = _parse_agent_file(content)

    backstory_parts = [
        _string_value(front_matter, "backstory"),
        body.strip() or None,
    ]
    backstory = "\n\n".join(part for part in backstory_parts if part)

    return AgentDefinition(
        name=_string_value(front_matter, "name"),
        description=_string_value(front_matter, "description"),
        backstory=backstory or None,
        model=_string_value(front_matter, "model"),
        bot_id=_string_value(front_matter, "botId")
        or _string_value(front_matter, "bot_id"),
        skillset_id=_string_value(front_matter, "skillsetId")
        or _string_value(front_matter, "skillset_id"),
        dataset_id=_string_value(front_matter, "datasetId")
        or _string_value(front_matter, "dataset_id"),
    )


def _resolve_file(file_path: str, roots: Iterable[str] | None) -> Path:
    path = Path(file_path)

    if path.is_absolute() and path.exists():
        return path

    for root in [Path.cwd(), *(Path(root) for root in roots or [])]:
        candidate = root / path

        if candidate.exists():
            return candidate

    raise FileNotFoundError(f"agent file not found: {file_path}")


def _parse_agent_file(content: str) -> tuple[dict[str, Any], str]:
    if not content.startswith("---"):
        return {}, content.strip()

    lines = content.splitlines()

    for index, line in enumerate(lines[1:], start=1):
        if line.strip() != "---":
            continue

        front_matter = _parse_front_matter("\n".join(lines[1:index]))
        body = "\n".join(lines[index + 1 :]).strip()

        return front_matter, body

    return {}, content.strip()


def _parse_front_matter(content: str) -> dict[str, Any]:
    result: dict[str, Any] = {}

    for raw_line in content.splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#") or ":" not in line:
            continue

        key, value = line.split(":", 1)
        value = value.strip()

        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value.startswith(("'", '"'))
        ):
            value = value[1:-1]

        result[key.strip()] = value

    return result


def _string_value(mapping: dict[str, Any], key: str) -> str | None:
    value = mapping.get(key)

    return value if isinstance(value, str) and value else None
