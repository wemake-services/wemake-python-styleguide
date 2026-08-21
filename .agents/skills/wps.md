---
name: wps
description: >
  wemake-python-styleguide (WPS) linting. Use when fixing flake8 `WPS` violations,
  or writing/reviewing Python in a repo where `wemake-python-styleguide` runs.
---

# wemake-python-styleguide

Edit Python until `flake8 --select=WPS,E999` reports nothing. Fix the code, not the config.

## Loop

1. Run `flake8 --select=WPS,E999 --format=default <paths>` with the project's flake8 config (`setup.cfg`, `.flake8`, or `[tool.flake8]` in `pyproject.toml`); pass `--isolated` only when the repo has none.
2. For each violation, edit the code so its cause is gone — the message names the rule and line; make the smallest change that satisfies it. When a rule's intent is unclear, read its page under the [violations index](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/violations/index.html), or call `explain_violation('WPS###')` if the WPS MCP server is running.
3. Re-run step 1. Done when it exits 0.

## Guardrails

- Suppress with `# noqa: WPS###` (the code, never bare `# noqa`) only when the user asks, or `per-file-ignores` already covers the line. Otherwise fix the code.
- Leave flake8 config untouched unless the user approves the edit. When one rule fires across many files and fixing each is wrong, propose a config change and wait.
- Delete a `# noqa: WPS###` once `flake8 --disable-noqa` shows its code no longer fires.

The `explain_violation` tool comes from the WPS MCP server: `pip install 'wemake-python-styleguide[mcp]'`, then register `mcp run wemake_python_styleguide/mcp_server.py:mcp` as a stdio server.
