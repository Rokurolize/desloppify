"""Command runtime context helpers for command handlers."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from desloppify.app.commands.helpers.state import state_path
from desloppify.base.config import load_config
from desloppify.base.runtime_state import current_runtime_context
from desloppify.engine.plan_state import resolve_plan_path_for_state
from desloppify.state_io import StateModel, load_state


@dataclass(frozen=True)
class CommandRuntime:
    """Explicit runtime dependencies shared by command handlers."""

    config: dict[str, Any]
    state: StateModel
    state_path: Path | None


def _bind_plan_file(runtime: CommandRuntime) -> None:
    """Keep implicit plan I/O aligned with the selected state file."""
    current_runtime_context().plan_file = (
        resolve_plan_path_for_state(runtime.state_path, migrate_legacy=True)
        if runtime.state_path is not None
        else None
    )


def command_runtime(args: argparse.Namespace) -> CommandRuntime:
    """Return runtime context from explicit args.runtime or construct one."""
    runtime = getattr(args, "runtime", None)
    if isinstance(runtime, CommandRuntime):
        _bind_plan_file(runtime)
        return runtime

    config = load_config()
    state_file = state_path(args)
    if isinstance(state_file, str):
        state_file = Path(state_file)

    state = load_state(state_file)

    runtime = CommandRuntime(config=config, state=state, state_path=state_file)
    _bind_plan_file(runtime)
    return runtime


__all__ = ["CommandRuntime", "command_runtime"]
