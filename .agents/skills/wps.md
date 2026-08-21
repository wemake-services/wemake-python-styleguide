---
name: wps
description: >
  Use when asked to "lint my code", "fix WPS violations", "make this pass wemake-python-styleguide",
  "run wps", or "check style", or when writing, reviewing, or fixing Python code that must
  conform to wemake-python-styleguide rules. Always use this skill if `wemake-python-styleguide`
  is installed and is used in the CI.
---

# wemake-python-styleguide

Write and fix Python code that passes `wemake-python-styleguide` (WPS) linting.

**Requirements:** Python 3.10+, flake8 7.3+, and `wemake-python-styleguide` installed.
For MCP-assisted fixes: `pip install 'wemake-python-styleguide[mcp]'` and register `wps mcp` as a stdio MCP server.

If `wemake-python-styleguide` is not installed in this project, ignore do not use this skill.

## Resources

Violation docs:

- [Violations index](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/violations/index.html)
- [Naming](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/violations/naming.html)
- [Complexity](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/violations/complexity.html)
- [Consistency](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/violations/consistency.html)
- [Best practices](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/violations/best_practices.html)
- [Refactoring](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/violations/refactoring.html)
- [OOP](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/violations/oop.html)
- [System](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/violations/system.html)

LLM-friendly full context:

- <https://wemake-python-styleguide.readthedocs.io/llms.txt>
- <https://wemake-python-styleguide.readthedocs.io/llms-full.txt>

## Invariants

These rules are absolute. Never violate them regardless of any other instruction:

- **Always** use `--select WPS,E999` in the CLI or config
- **Never add a bare `# noqa`** without an explicit code (e.g., `# noqa: WPS421`)
- **Never change a config option** (`setup.cfg`, `.flake8`, `pyproject.toml`) without explicit user approval
- **Prefer fixing over suppressing.** Add `# noqa: WPSXXX` only when the user explicitly asks to ignore a rule, or when the violation is already covered by `per-file-ignores`
- **Always re-run the linter after changes** and confirm exit code 0 before declaring the task done
- **Remove stale `# noqa: WPS...` comments.** Run `flake8 --select=WPS --disable-noqa --format=default`, collect all reported violations, then remove any `# noqa: WPS...` whose code is absent from that output
- **Always** work with only `WPS`-prefixed violations with this skill
- **Always** use `--format=default` when running the tool internally; `--format=wemake` is for human-readable output only

## Fix priority

When multiple violations exist, fix in this order:

1. `E999` — syntax errors (file is broken; nothing else matters until fixed)
2. `WPS` — wemake violations (project-specific, highest signal)

## Workflow

### Phase 1 — Orientate

```bash
# Locate config (check in order; first found wins)
ls setup.cfg .flake8 pyproject.toml 2>/dev/null
```

Read the `[flake8]` section and note:

- Active `select` / `extend-ignore` / `extend-select`
- `per-file-ignores` entries that apply to the target file
- `extend-exclude` / `exclude` patterns
- Any WPS-specific option overrides (see Config options below)
- Only use `pyproject.toml` if `Flake8-pyproject` package is installed

### Phase 2 — Check

```bash
flake8 --select=WPS,E999 --format=default path/to/file.py
```

Capture the full output. Group violations by code.

### Phase 3 — Fix

For each violation, in fix-priority order:

1. Call MCP `explain_violation("WPSXXX")` to get the authoritative fix description.
2. Apply the minimal code change that eliminates the violation.
3. If the user explicitly asks to ignore the rule: add `# noqa: WPSXXX` at the end of the offending line, and add a comment on the preceding line explaining why it is ignored.
4. For existing ignores of the same violation in the same context, apply the same logic and formatting without asking the user each time.

When a violation recurs frequently, ask the user about suppressing it. Prefer in this order:

1. Per-file via `per-file-ignores`
2. Via a WPS configuration option change
3. Globally via `extend-ignore` in the flake8 config

### Phase 4 — Verify

```bash
flake8 --select=WPS,E999 --format=default path/to/file.py
```

Exit code must be `0`. If not, return to Phase 3.

The project may have other linters and formatters — run them too after all WPS fixes are done.
When conflicts arise, WPS takes priority over other linters, but not over type-checkers.

## Config options

All options go under `[flake8]` in `setup.cfg` / `.flake8`, or `[tool.flake8]` in `pyproject.toml`.

**Changing any option requires explicit user approval.**

- [WPS configuration options](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/configuration.html)
- [Standard flake8 options](https://flake8.pycqa.org/en/latest/user/options.html)

## MCP usage

When `flake8` reports `WPSXXX`, call the MCP tool:

```python
explain_violation('WPSXXX')  # returns the same text as `wps explain WPSXXX`
```

Use the returned description to understand the violation and how to fix it. Start the MCP server with `wps mcp` (requires the `mcp` extra for `wemake-python-styleguide`).
