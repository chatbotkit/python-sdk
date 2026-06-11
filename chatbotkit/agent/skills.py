from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class SkillDefinition:
    name: str
    description: str
    path: str


@dataclass
class SkillsResult:
    skills: list[SkillDefinition] = field(default_factory=list)
    directories: list[str] = field(default_factory=list)

    def reload(self) -> None:
        self.skills = _scan_directories(self.directories)


def load_skills(directories: Iterable[str]) -> SkillsResult:
    directory_list = list(directories)

    return SkillsResult(
        skills=_scan_directories(directory_list),
        directories=directory_list,
    )


def create_skills_feature(skills: Iterable[SkillDefinition]) -> dict[str, Any]:
    return {
        "name": "skills",
        "options": {
            "skills": [
                {
                    "name": skill.name,
                    "description": skill.description,
                    "path": skill.path,
                }
                for skill in skills
            ]
        },
    }


def _scan_directories(directories: Iterable[str]) -> list[SkillDefinition]:
    skills: list[SkillDefinition] = []

    for directory in directories:
        base_path = Path(directory).expanduser().resolve()

        if not base_path.is_dir():
            continue

        for child in sorted(base_path.iterdir()):
            if not child.is_dir():
                continue

            skill = _load_skill(child)

            if skill is not None:
                skills.append(skill)

    return skills


def _load_skill(directory: Path) -> SkillDefinition | None:
    skill_file = directory / "SKILL.md"

    if not skill_file.is_file():
        return None

    content = skill_file.read_text(encoding="utf-8")
    front_matter = _parse_front_matter(content)
    name = front_matter.get("name")
    description = front_matter.get("description")

    if not isinstance(name, str) or not isinstance(description, str):
        return None

    if not name or not description:
        return None

    return SkillDefinition(
        name=name,
        description=description,
        path=str(directory),
    )


def _parse_front_matter(content: str) -> dict[str, str]:
    if not content.startswith("---"):
        return {}

    lines = content.splitlines()

    for index, line in enumerate(lines[1:], start=1):
        if line.strip() != "---":
            continue

        return _parse_simple_yaml("\n".join(lines[1:index]))

    return {}


def _parse_simple_yaml(content: str) -> dict[str, str]:
    result: dict[str, str] = {}

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
