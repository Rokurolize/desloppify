"""Sanity tests for the SCSS language plugin."""

from __future__ import annotations

import pytest

from desloppify.languages import get_lang


@pytest.fixture(scope="module")
def cfg():
    return get_lang("scss")


def test_stylelint_uses_project_local_binary(cfg):
    detect_fn = cfg.detect_commands["stylelint_issue"]
    freevars = detect_fn.__code__.co_freevars
    cmd: str = detect_fn.__closure__[freevars.index("cmd")].cell_contents
    assert cmd.startswith("npx --no-install stylelint ")


def test_fix_cmd_uses_project_local_binary(cfg):
    fix_fn = next(iter(cfg.fixers.values())).fix
    freevars = fix_fn.__code__.co_freevars
    fix_cmd: str = fix_fn.__closure__[freevars.index("fix_cmd")].cell_contents
    assert fix_cmd.startswith("npx --no-install stylelint ")
