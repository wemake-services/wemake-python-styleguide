---
name: wemake-python-styleguide
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

Violation docs (always current — do not rely on a hard-coded list):

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

1. **Never add a bare `# noqa`** without an explicit code (e.g., `# noqa: WPS421`).
2. **Never remove an existing `# noqa` marker** — the project owner put it there intentionally.
3. **Never change a config option** (`setup.cfg`, `.flake8`, `pyproject.toml`) without explicit user approval.
4. **Prefer fixing over suppressing.** Only add `# noqa: WPSXXX` when the user explicitly asks to ignore a rule, or when the violation is already covered by `per-file-ignores`.
5. **Always re-run the linter after every change** and confirm exit code 0 before declaring the task done.

## Output format

```
path/to/file.py:10:5: WPS421 Found `print` call
```

Fields: `<file>:<line>:<col>: <code> <message>`

Code prefixes and their meaning:

| Prefix | Source | Signal |
|---|---|---|
| `WPS` | wemake-python-styleguide | Primary — fix these first |
| `E999` | flake8 syntax error | Critical — file cannot be parsed |
| `E` / `W` | pycodestyle | Secondary — formatting |
| `F` | pyflakes | Secondary — undefined/unused names |

Exit codes: `0` = clean, `1` = violations found, any other = tool/config error.

## Fix priority

When multiple violations exist, fix in this order:

1. `E999` — syntax errors (file is broken; nothing else matters until fixed)
2. `WPS` — wemake violations (project-specific, highest signal)
3. `F` — undefined/unused names
4. `E` / `W` — formatting

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

### Phase 2 — Check

```bash
flake8 --select=WPS,E999 path/to/file.py
```

Capture the full output. Group violations by code.

### Phase 3 — Fix

For each violation, in fix-priority order:

1. Call MCP `explain_violation("WPSXXX")` to get the authoritative fix description.
2. Apply the minimal code change that eliminates the violation.
3. If a `per-file-ignores` entry already covers this file+code, skip — no fix needed.
4. If the user explicitly asks to ignore the rule: add `# noqa: WPSXXX  # reason` at the end of the offending line.

### Phase 4 — Verify

```bash
flake8 --select=WPS,E999 path/to/file.py
```

Exit code must be `0`. If not, return to Phase 3.

## Config options

All options go under `[flake8]` in `setup.cfg` / `.flake8`, or `[tool.flake8]` in `pyproject.toml`.

**Changing any option requires explicit user approval.**

### General

| Option | Default | Description |
|---|---|---|
| `min-name-length` | `2` | Minimum variable/module name length |
| `max-name-length` | `45` | Maximum variable/module name length |
| `max-noqa-comments` | `10` | Maximum `# noqa` comments per module |
| `nested-classes-whitelist` | `Meta, Params, Config` | Allowed nested class names |
| `allowed-domain-names` | *(empty)* | Names removed from the generic-names blacklist |
| `forbidden-domain-names` | *(empty)* | Names added to the generic-names blacklist |
| `allowed-module-metadata` | *(empty)* | Allowed module-level dunder names |
| `forbidden-module-metadata` | *(empty)* | Forbidden module-level dunder names |
| `forbidden-inline-ignore` | *(empty)* | `noqa` codes forbidden from being silenced inline |
| `exps-for-one-empty-line` | `2` | Max expressions allowed before an empty line inside a function |
| `known-enum-bases` | *(empty)* | Additional base class names treated as enums |

### Complexity

| Option | Default | Description |
|---|---|---|
| `max-returns` | `5` | Max `return` statements per function |
| `max-local-variables` | `5` | Max local variables per function |
| `max-expressions` | `9` | Max expressions per function |
| `max-arguments` | `5` | Max arguments per function/method |
| `max-module-members` | `7` | Max classes + functions per module |
| `max-methods` | `7` | Max methods per class |
| `max-line-complexity` | `14` | Max Jones complexity per line |
| `max-jones-score` | `12` | Max median Jones complexity per module |
| `max-imports` | `12` | Max import statements per module |
| `max-imported-names` | `50` | Max total imported names per module |
| `max-base-classes` | `3` | Max base classes |
| `max-decorators` | `5` | Max decorators per function/class |
| `max-string-usages` | `3` | Max identical string literal uses |
| `max-awaits` | `5` | Max `await` expressions per function |
| `max-try-body-length` | `1` | Max statements in a `try` block body |
| `max-module-expressions` | `7` | Max repeated expressions per module |
| `max-function-expressions` | `4` | Max repeated expressions per function |
| `max-asserts` | `5` | Max `assert` statements per function |
| `max-access-level` | `4` | Max chained attribute access depth |
| `max-attributes` | `6` | Max public attributes per class |
| `max-raises` | `3` | Max `raise` statements per function |
| `max-except-exceptions` | `3` | Max exception types per `except` clause |
| `max-cognitive-score` | `12` | Max cognitive complexity per function |
| `max-cognitive-average` | `8` | Max average cognitive complexity per module |
| `max-call-level` | `3` | Max chained call depth |
| `max-annotation-complexity` | `3` | Max nesting depth of type annotations |
| `max-import-from-members` | `8` | Max names imported from a single module |
| `max-tuple-unpack-length` | `4` | Max variables in a tuple unpacking |
| `max-type-params` | `6` | Max PEP 695 type parameters |
| `max-match-subjects` | `7` | Max subjects in a `match` statement |
| `max-match-cases` | `7` | Max `case` branches in a `match` statement |
| `max-lines-in-finally` | `2` | Max statements in a `finally` block |
| `max-conditions` | `4` | Max conditions in a single `if`/`while` |

### Formatter

| Option | Default | Description |
|---|---|---|
| `show-violation-links` | `False` | Show doc links in formatter output |

### Standard flake8 options (also respected)

`per-file-ignores`, `extend-exclude`, `exclude`, `max-line-length`, `select`, `extend-ignore`, `extend-select`

## MCP usage

When `flake8` reports `WPSXXX`, call the MCP tool:

```python
explain_violation("WPSXXX")  # returns the same text as `wps explain WPSXXX`
```

Use the returned description to understand what is wrong and how to fix it. The MCP server is started with `wps mcp` (requires the `mcp` extra).
