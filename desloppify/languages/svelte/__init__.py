"""Svelte component language plugin."""

from __future__ import annotations

from desloppify.languages._framework.generic_support.core import generic_lang

cfg = generic_lang(
    name="svelte",
    extensions=[".svelte"],
    tools=[
        {
            "label": "Svelte Check",
            "cmd": "npx --no-install svelte-check --output machine",
            "fmt": "svelte_check",
            "id": "svelte_check_issue",
            "tier": 2,
        },
        {
            "label": "ESLint",
            "cmd": "npx --no-install eslint '**/*.svelte' --format json --no-error-on-unmatched-pattern",
            "fmt": "eslint",
            "id": "svelte_eslint_warning",
            "tier": 2,
            "fix_cmd": "npx --no-install eslint '**/*.svelte' --fix --no-error-on-unmatched-pattern",
        },
    ],
    exclude=["node_modules", ".svelte-kit", "dist", "build", "coverage"],
    depth="shallow",
    detect_markers=["svelte.config.js", "svelte.config.ts"],
    default_src="src",
)

__all__ = [
    "cfg",
    "generic_lang",
]
