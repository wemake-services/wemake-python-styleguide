# Skill: wemake-python-styleguide

Write Python code that passes `wemake-python-styleguide` (WPS) linting.

## Resources

Violation docs (always current, use these — do not rely on a hard-coded list):

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

## Setup

```bash
pip install 'wemake-python-styleguide[mcp]'
```

Register the MCP server (`wps mcp`) in your agent config to use `explain_violation`.

## Workflow

1. **Load config** — read `setup.cfg` / `.flake8` / `pyproject.toml [tool.flake8]` and note all option values, `per-file-ignores`, `extend-exclude`, and inline `# noqa` markers. **Do not change any config without explicit user approval.**
2. **Write code** — follow all WPS rules (see violation docs above).
3. **Check** — run `flake8 --select=WPS,E999 <file>` and capture violations.
4. **Fix each violation** — call MCP `explain_violation("WPSXXX")` to get the fix description, then fix the code. Prefer fixing over `# noqa`. Only add `# noqa: WPSXXX` when the user explicitly asks to ignore a rule or a `per-file-ignores` entry already covers it.
5. **Re-check** until clean.

## Config options

All options go under `[flake8]` in `setup.cfg` / `.flake8` (or `[tool.flake8]` in `pyproject.toml`).

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

## Config awareness

Before writing or fixing code:

- Read `setup.cfg` / `.flake8` / `pyproject.toml` for active option values.
- Respect existing `# noqa: WPSXXX` inline markers — do not remove them.
- If a rule is listed under `per-file-ignores` for the current file, it does not need to be fixed.
- **Never change config values without the user's explicit approval.**

## MCP usage

When `flake8` reports `WPSXXX`:

1. Call `explain_violation("WPSXXX")` to get the fix description.
2. Fix the code based on the explanation.
3. Only if a fix is impossible **and** the user explicitly asks to ignore it: add `# noqa: WPSXXX`.
