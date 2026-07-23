"""Packaging metadata invariants for required package data."""

from __future__ import annotations

import tomllib
from pathlib import Path

from desloppify.app.skill_docs import SKILL_VERSION, SKILL_VERSION_RE


def _package_data() -> dict[str, list[str]]:
    pyproject_path = Path(__file__).resolve().parents[3] / "pyproject.toml"
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    package_data = data.get("tool", {}).get("setuptools", {}).get("package-data", {})
    assert isinstance(package_data, dict), "tool.setuptools.package-data must be a table"
    return package_data


def test_visualization_template_is_packaged() -> None:
    package_data = _package_data()
    template_files = package_data.get("desloppify.app.output")
    assert isinstance(template_files, list), (
        "desloppify.app.output package data must be declared in pyproject.toml"
    )
    assert "_viz_template.html" in template_files


def test_global_skill_documents_are_packaged() -> None:
    package_data = _package_data()
    skill_files = package_data.get("desloppify.data.global")
    assert isinstance(skill_files, list), (
        "desloppify.data.global package data must be declared in pyproject.toml"
    )
    assert "*.md" in skill_files


def test_bundled_skill_matches_canonical_document_and_version() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    canonical = (repo_root / "docs" / "SKILL.md").read_text(encoding="utf-8")
    bundled = (
        repo_root / "desloppify" / "data" / "global" / "SKILL.md"
    ).read_text(encoding="utf-8")

    assert bundled == canonical
    version_match = SKILL_VERSION_RE.search(canonical)
    assert version_match is not None
    assert int(version_match.group(1)) == SKILL_VERSION
