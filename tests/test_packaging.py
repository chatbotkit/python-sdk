from __future__ import annotations

import importlib.util
import py_compile
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib

import httpx
import pytest

from chatbotkit import ChatBotKit
from chatbotkit.agent import create_skills_feature, load_agent, load_skills

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.asyncio
async def test_client_public_surface_imports_and_initializes():
    async with ChatBotKit(
        secret="cbk_test",
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json={})),
    ) as cbk:
        for name in [
            "bot",
            "conversation",
            "dataset",
            "skillset",
            "file",
            "contact",
            "secret",
            "memory",
            "blueprint",
            "task",
            "team",
            "space",
            "partner",
            "policy",
            "portal",
            "usage",
            "magic",
            "event",
            "graphql",
            "channel",
            "platform",
            "integration",
        ]:
            assert hasattr(cbk, name)


def test_package_and_examples_compile():
    paths = [
        *sorted((ROOT / "chatbotkit").rglob("*.py")),
        *sorted((ROOT / "examples").rglob("*.py")),
    ]

    for path in paths:
        if "__pycache__" in path.parts:
            continue

        py_compile.compile(str(path), doraise=True)


def test_examples_import_without_running_main():
    for path in sorted((ROOT / "examples").rglob("*.py")):
        if "__pycache__" in path.parts:
            continue

        module_name = "example_" + "_".join(path.relative_to(ROOT).with_suffix("").parts)
        spec = importlib.util.spec_from_file_location(module_name, path)

        assert spec is not None
        assert spec.loader is not None

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)


def test_example_agent_assets_load():
    agent = load_agent(
        "assistant.md",
        roots=[str(ROOT / "examples" / "agent" / "agents")],
    )

    assert agent.name == "Launch Assistant"
    assert agent.model == "gpt-4o"
    assert agent.backstory

    skills = load_skills([str(ROOT / "examples" / "agent" / "skills")]).skills
    feature = create_skills_feature(skills)

    assert {skill.name for skill in skills} == {"code-review", "summarize"}
    assert feature["name"] == "skills"
    assert len(feature["options"]["skills"]) == 2


def test_pyproject_extras_are_publish_ready():
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = pyproject["project"]
    extras = project["optional-dependencies"]

    assert project["name"] == "chatbotkit"
    assert project["requires-python"] == ">=3.10"
    assert "pydantic>=2.7" in extras["agent"]
    assert "python-dotenv>=1.0" in extras["examples"]
    assert "build>=1.2" in extras["dev"]
    assert "twine>=5" in extras["dev"]
