"""Tests for first-class Svelte component scanning."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from desloppify.languages import get_lang
from desloppify.languages._framework.generic_parts.parsers import (
    ToolParserError,
    parse_svelte_check,
)
from desloppify.languages._framework.generic_parts.tool_runner import (
    run_tool_result,
)


@pytest.fixture(scope="module")
def cfg():
    return get_lang("svelte")


def test_svelte_is_a_first_class_language(cfg, tmp_path):
    component = tmp_path / "src" / "Counter.svelte"
    component.parent.mkdir()
    component.write_text("<button>{count}</button>\n")
    assert cfg.extensions == [".svelte"]
    discovered = cfg.file_finder(tmp_path)
    assert len(discovered) == 1
    assert Path(discovered[0]).resolve() == component.resolve()


def test_svelte_tools_are_component_scoped(cfg):
    labels = {phase.label for phase in cfg.phases}
    assert {"Svelte Check", "ESLint"} <= labels
    eslint_fn = cfg.detect_commands["svelte_eslint_warning"]
    freevars = eslint_fn.__code__.co_freevars
    cmd: str = eslint_fn.__closure__[freevars.index("cmd")].cell_contents
    assert "**/*.svelte" in cmd
    assert "eslint ." not in cmd


def test_parse_svelte_check_filters_sibling_languages():
    output = "\n".join(
        [
            '100 START "/project"',
            '101 ERROR "src/App.svelte" 8:4 "Unknown property"',
            '102 WARNING "src/helper.ts" 3:1 "Unused value"',
            "103 COMPLETED 1 FILES 1 ERRORS 0 WARNINGS 1 DURATION",
        ]
    )
    entries, meta = parse_svelte_check(output, Path("."))
    assert entries == [
        {
            "file": "src/App.svelte",
            "line": 8,
            "message": "[error] Unknown property",
        }
    ]
    assert meta["potential"] == 1
    assert meta["allow_empty_nonzero"] is True


def test_parse_svelte_check_rejects_unrecognized_output():
    with pytest.raises(ToolParserError):
        parse_svelte_check("npm ERR! missing script", Path("."))


def test_clean_svelte_subset_accepts_diagnostic_exit(tmp_path):
    output = "\n".join(
        [
            '100 START "/project"',
            '101 ERROR "src/helper.ts" 3:1 "Unused value"',
            "102 COMPLETED 1 FILES 1 ERRORS 0 WARNINGS 1 DURATION",
        ]
    )

    def run_subprocess(*_args, **_kwargs):
        return subprocess.CompletedProcess(
            args=["svelte-check"],
            returncode=1,
            stdout=output,
            stderr="",
        )

    result = run_tool_result(
        "svelte-check --output machine",
        tmp_path,
        parse_svelte_check,
        run_subprocess=run_subprocess,
    )
    assert result.status == "empty"
    assert result.error_kind is None
