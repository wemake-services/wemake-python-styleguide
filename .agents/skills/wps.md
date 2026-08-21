---
name: wps
description: >
  Use when a user says "lint my code", "fix WPS violations", "make this pass wemake-python-styleguide",
  "run wps", "check style", or asks to write, review, or fix Python code that must conform to
  wemake-python-styleguide rules.
compatibility: >
  Requires Python 3.10+, flake8 7.3+, and wemake-python-styleguide installed.
  For MCP-assisted fixes: install with `pip install 'wemake-python-styleguide[mcp]'`
  and register `wps mcp` as a stdio MCP server.
---

# Skill: wemake-python-styleguide

Write and fix Python code that passes `wemake-python-styleguide` (WPS) linting.

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

- Make sure that `--select WPS, E999` in the CLI or in the config is **always** used
- **Never add a bare `# noqa`** without an explicit code (e.g., `# noqa: WPS421`).
- **Never change a config option** (`setup.cfg`, `.flake8`, `pyproject.toml`) without explicit user approval.
- **Prefer fixing over suppressing.** Only add `# noqa: WPSXXX` when the user explicitly asks to ignore a rule, or when the violation is already covered by `per-file-ignores`.
- **Always re-run the linter after changes** and confirm exit code 0 before declaring the task done.
- Remove `# noqa` comments that no longer apply. To test this run `flake8 --select=WPS --disable-noqa --format=default`, remember all reported violations, compare them with the list of `# noqa: WPS` comments
- **Always** work with only `WPS` prefixed violations with this skill
- **Always** prefer the default `--format=default` option when running the tool internally, `--format=wemake` is only helpful for humans

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
3. If the user explicitly asks to ignore the rule: add `# noqa: WPSXXX` at the end of the offending line. And add a comment before the line with the `# noqa` with reasoning, why this is ignored
4. If there are existing ignores for the same violations in the same context, apply the same logic and formatting to new ones, without asking the user on each similar violation

If some violations happens a lot, ask a user if they want to ignore it, priority:

1. Per file with `per-file-ignores`
2. With changing configuration option
3. Globally in `extend-ignore` flake8's configuration

### Phase 4 — Verify

```bash
flake8 --select=WPS,E999 --format=default path/to/file.py
```

Exit code must be `0`. If not, return to Phase 3.

Make sure that the project might have other linters and formatters.
Run them as well after all fixes are done.
When there are conflicts, prioritize WPS over other linters, but not type-checkers.

## Config options

All options go under `[flake8]` in `setup.cfg` / `.flake8`, or `[tool.flake8]` in `pyproject.toml`.

**Changing any option requires explicit user approval.**

List of all options:

- [Configuration options](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/configuration.html)


### Standard flake8 options (also respected)

- [Flake8 options](https://flake8.pycqa.org/en/latest/user/options.html)

## MCP usage

When `flake8` reports `WPSXXX`, call the MCP tool:

```python
explain_violation('WPSXXX')  # returns the same text as `wps explain WPSXXX`
```

Use the returned description to understand what is wrong and how to fix it. The MCP server is started with `wps mcp` (requires the `mcp` extra for `wemake-python-styleguide`).
