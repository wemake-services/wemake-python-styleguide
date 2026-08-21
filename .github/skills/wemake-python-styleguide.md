# Skill: wemake-python-styleguide

Write Python code that passes `wemake-python-styleguide` (WPS) linting.

## Setup

```bash
pip install 'wemake-python-styleguide[mcp]'
```

Register the MCP server (`wps mcp`) in your agent config to use `explain_violation`.

## Workflow

1. **Load config** — read `setup.cfg` / `.flake8` / `pyproject.toml` for:
   - `extend-exclude`, `per-file-ignores`, `max-*` option overrides, `noqa` inline markers.
2. **Write code** — follow all WPS rules below.
3. **Check** — run `flake8 --select=WPS,E999 <file>` and capture violations.
4. **Fix each violation** — call MCP `explain_violation("WPSXXX")` to get the description, then fix the code. Prefer fixing over `# noqa`. Only add `# noqa: WPSXXX` when the user explicitly asks to ignore a rule or a `per-file-ignores` entry already covers it.
5. **Re-check** until clean.

## Rules summary

### Naming (WPS1xx)

- `WPS100` — no single-char names except loop vars (`i`, `j`, `k`, `_`)
- `WPS101` — no consecutive underscores in names
- `WPS102` — module names: lowercase, no numbers
- `WPS110` — no generic names (`data`, `result`, `value`, `item`, `obj`, `info`, `handler`, `manager`, `response`, `request`, `input`, `output`, `res`, `ret`, `val`, `var`, `tmp`, `temp`, `d`, `f`, `x`, `y`, `z`, `n`, `el`, `element`, `err`, `exc`, `e`, `ex`, `exception`, `error`)
- `WPS111` — no too-short names (default min length: 2)
- `WPS112` — no private module names (leading `_`)
- `WPS113` — no same names in nested scopes
- `WPS114` — no underscored-number names
- `WPS115` — no upper-case constants in classes
- `WPS116` — no consecutive underscores
- `WPS117` — no `__` name
- `WPS118` — no too-long names (default max: 45 chars)
- `WPS119` — no undescriptive variable names (single-letter in non-loop context)
- `WPS120` — no regular names with trailing `_`
- `WPS121` — no protected module names
- `WPS122` — no unused variables (assign and never use; use `_` prefix)
- `WPS123` — no `__all__` with non-string members
- `WPS124` — no variable re-assignments inside loops
- `WPS125` — no builtin shadowing (`list`, `dict`, `id`, `type`, etc.)

### Complexity (WPS2xx)

- `WPS200` — no too-complex modules (many members)
- `WPS201` — max imports per module: 12
- `WPS202` — max module members: 7
- `WPS203` — max imported names per `from` import: 8
- `WPS204` — max expression uses: 7 (avoid repeating the same expression)
- `WPS210` — max local variables per function: 5
- `WPS211` — max arguments per function: 5
- `WPS212` — max returns per function: 3
- `WPS213` — max expressions per function: 9
- `WPS214` — max methods per class: 7
- `WPS215` — max base classes: 3
- `WPS216` — max decorators: 5
- `WPS217` — max await expressions: 5
- `WPS218` — max asserts: 5
- `WPS219` — max access level (chained attribute access): 4
- `WPS220` — max cognitive complexity of a function: 12
- `WPS221` — max Jones complexity of a line: 14
- `WPS222` — max conditions in `if`: 3
- `WPS223` — max `elif` branches: 3
- `WPS224` — max comprehension operators: 2
- `WPS225` — max string token usages: 3
- `WPS226` — no string constant over-use (3 or more identical strings)
- `WPS227` — max function length: 20 lines
- `WPS228` — max module length: 400 lines
- `WPS229` — max `try` body length: 1
- `WPS230` — max `__init__` arguments: 10
- `WPS231` — max function complexity: 12 (cyclomatic)
- `WPS232` — max module complexity
- `WPS233` — max locals in comprehension: 2
- `WPS234` — overuse of noqa comments
- `WPS235` — max `except` handlers: 3
- `WPS236` — max tuple unpacking length: 4
- `WPS237` — max `for` loop variables: 2
- `WPS238` — max raises: 3
- `WPS239` — max annotation complexity
- `WPS240` — max generic types in annotation
- `WPS241` — max base class length
- `WPS242` — max inner classes
- `WPS243` — max decorators on a class

### Complexity continued (WPS3xx — consistency)

_(see the Consistency section below)_

### Best practices (WPS4xx)

- `WPS400` — no wrong magic comments (e.g. `# type: ignore`, `# noqa` without a code)
- `WPS401` — no `__future__` imports
- `WPS402` — no `noqa` comments without a reason
- `WPS403` — no `# type: ignore` without a reason
- `WPS404` — no mutable module constants (list, dict, set literals at module level)
- `WPS405` — no global/nonlocal
- `WPS406` — no non-`__all__` imports in `__init__.py` of external modules
- `WPS407` — no mutable class attributes as class-level assignments
- `WPS408` — no duplicate conditions
- `WPS409` — no `except Exception` (too broad)
- `WPS410` — no `__all__` in non-`__init__` modules
- `WPS411` — no empty comments
- `WPS412` — no logic inside `__init__` modules (only imports and `__all__` allowed)
- `WPS413` — no `__getattr__` or `__dir__` module-level magic methods
- `WPS414` — no incorrect `unpacking` target
- `WPS415` — no incorrect `for` loop target
- `WPS416` — no `yield` inside comprehension
- `WPS417` — no non-unique conditions in `if-elif`
- `WPS418` — no non-unique items in a set
- `WPS419` — no `finally` in try block without `except`
- `WPS420` — no `pass` usage (except empty bodies)
- `WPS421` — no `print()` calls
- `WPS422` — no `breakpoint()` calls
- `WPS423` — no `raise NotImplemented` (use `NotImplementedError`)
- `WPS424` — no `BaseException` in `raise` or `except`
- `WPS425` — no boolean non-default args (`bool` as function arg with literal default)
- `WPS426` — no `lambda` inside loops
- `WPS427` — no `for` / `while` with `else`
- `WPS428` — no statements that are plain expressions (not assignments)
- `WPS429` — no multiple assignments on one line
- `WPS430` — no nested functions
- `WPS431` — no nested classes
- `WPS432` — no magic numbers
- `WPS433` — no nested imports (imports inside functions)
- `WPS434` — no `return` with assignment expression
- `WPS435` — no `continue` in loops
- `WPS436` — no `__version__` outside `__init__.py`
- `WPS437` — no protected attribute access (`obj._attr`)
- `WPS438` — no `__del__`
- `WPS439` — no `type: ignore` in comments
- `WPS440` — no block variable overlap (same var in `for` and outer scope)
- `WPS441` — no control variables after the loop
- `WPS442` — no shadowing outer scope in fixtures/closures
- `WPS443` — no pointless `starred` expressions
- `WPS444` — no keyword arguments in some operators
- `WPS445` — no incorrect `unpacking` in `with`
- `WPS446` — approximate constants (use `math.pi`, `math.e` etc.)
- `WPS447` — no unsafe `*` in `__all__`
- `WPS448` — no incorrect `except` ordering
- `WPS449` — no `float` in `except`
- `WPS450` — no plain `raise` without exception inside `finally`
- `WPS451` — no positional-only args before Python 3.8
- `WPS452` — no `break` in `for`/`while` `else`
- `WPS453` — no executable `if __name__ == '__main__'` inside modules
- `WPS454` — no wrong `raise` inside `finally`
- `WPS455` — no non-trivial expressions in starred assignments
- `WPS456` — no `nan` comparisons
- `WPS457` — no infinite `while True` loops
- `WPS458` — no same-name imports `import x; import x`
- `WPS459` — no comparisons with `None` / `True` / `False` via `==`; use `is` / `is not`
- `WPS460` — no `X is not None` replaced by truthiness check (opposite: prefer explicit)
- `WPS461` — no control flow in `finally`
- `WPS462` — no unneeded `else` after `return`/`raise`/`continue`
- `WPS463` — no `get()` with default for non-dict types
- `WPS464` — no empty line after a decorator
- `WPS465` — no bitwise operations
- `WPS466` — no `mutable` default arguments
- `WPS467` — no bare `raise` outside `except`
- `WPS468` — no `__bool__` that doesn't return bool
- `WPS469` — no `yield` / `yield from` mixed
- `WPS470` — no implicit `return None`
- `WPS471` — no indexed iteration (`range(len(x))`); use `enumerate`
- `WPS472` — no implicit `in` comparison (use explicit `in`)
- `WPS473` — no `__init__` with return value
- `WPS474` — no `assert False` / `assert True`
- `WPS475` — no `super()` with explicit class and self
- `WPS476` — no `__slots__` in non-final classes
- `WPS477` — no `__all__` members that are not defined
- `WPS478` — no implicit `__init__` calls via `__class__`
- `WPS479` — no `next(iter(...))` (use other patterns)
- `WPS480` — no `type` builtin used for dynamic class creation
- `WPS481` — no `re.compile()` at module level without assigning to a constant
- `WPS482` — no lazy imports (imports inside `if TYPE_CHECKING` that aren't type-only)

### OOP (WPS5xx)

- `WPS500` — no `__init__` that only calls `super()`
- `WPS501` — no bare `super()` call without overriding
- `WPS502` — no multiple return types
- `WPS503` — no useless `return None`
- `WPS504` — no negated conditions (`if not x: ... else: ...` → invert)
- `WPS505` — no nested `return`
- `WPS506` — no useless `lambda`
- `WPS507` — no useless `len()` comparison (`if len(x) > 0`)
- `WPS508` — no `not ... in ...` (use `not in`)
- `WPS509` — no `not ... is ...` (use `is not`)
- `WPS510` — no `in` with literal singleton (use `== val`)
- `WPS511` — no non-unique items in `isinstance` tuple
- `WPS512` — no `isinstance` with a single-element tuple
- `WPS513` — no wrong `except` handler
- `WPS514` — no implicit complex comparison (`if a and b and a`)
- `WPS515` — no `open()` without explicit `mode`
- `WPS516` — no `self` as a default argument
- `WPS517` — no `__slots__` containing `__dict__`
- `WPS518` — no `enumerate()` with custom start in certain patterns
- `WPS519` — no `max()`/`min()` comparisons
- `WPS520` — no `sum()` / `any()` / `all()` anti-patterns
- `WPS521` — no `is` comparison with literals
- `WPS522` — no implicit primitives (`True == x` instead of `x`)
- `WPS523` — no starred assignment in `return`
- `WPS524` — no same value in `__init__` self-assignment (`self.x = x` where `x` and `self.x` are the same)
- `WPS525` — no `in` with single-element tuple
- `WPS526` — no `yield` from `return` in generator
- `WPS527` — no `zip()` without `strict=` (Python 3.10+)
- `WPS528` — no implicit `.items()` (iterating dict without `.items()`)
- `WPS529` — no index-zero slicing (`x[0:n]` instead of `x[:n]`)
- `WPS530` — no incorrect `__iter__` return type
- `WPS531` — no `simplifiable_if` (if returning bool based on bool condition)
- `WPS532` — no `reversed(sorted(...))` (use `sorted(..., reverse=True)`)
- `WPS533` — no outer scope names shadowed via comprehension variable
- `WPS534` — no `return` in `__init__`
- `WPS535` — no missing `await` expression
- `WPS536` — no incorrect `super()` signature

### Consistency (WPS3xx)

- `WPS300` — no relative imports
- `WPS301` — no `import` of non-module (e.g. `import os.path.join`)
- `WPS302` — no `u""` unicode string prefix
- `WPS303` — no underscores in numeric literals (`1_000_000` is OK; `1__000` is not)
- `WPS304` — no partial `float` literals (`.5` or `5.`)
- `WPS305` — no `f""` without format vars
- `WPS306` — no `class Foo(object):`; use `class Foo:`
- `WPS307` — no `__future__` imports
- `WPS308` — no `yield` in `return` statement
- `WPS309` — no reversed comparison (`0 < x` → use `x > 0`)
- `WPS310` — no `else` in a function after `return`/`raise`
- `WPS311` — no `and`/`or` with the same left part
- `WPS312` — no `len()` in boolean context (`if len(x):` → `if x:`)
- `WPS313` — no `not` inside `all()`/`any()` (simplify)
- `WPS314` — no explicit string concatenation in `__all__`
- `WPS315` — no extra `+` or `-` in unary expressions
- `WPS316` — no context manager variable assigned to `_`
- `WPS317` — no incorrect `else` for `try`
- `WPS318` — no extra indentation
- `WPS319` — no bracket-first coding style (closing bracket position)
- `WPS320` — no multiline conditions
- `WPS321` — no uppercase string modifier (`B""`, `U""`)
- `WPS322` — no `\` line continuations; use brackets
- `WPS323` — no `%` string formatting
- `WPS324` — no `return` with boolean literal
- `WPS325` — no implicit `yield` (yield without value)
- `WPS326` — no implicit string concatenation (`"foo" "bar"`)
- `WPS327` — no `continue` in `finally`
- `WPS328` — no `pass` in `except`
- `WPS329` — no meaningless `continue`
- `WPS330` — no `not` with unary operators
- `WPS331` — no unnecessary `elif` after `return`
- `WPS332` — no walrus operator (`:=`) in some contexts
- `WPS333` — no implicit `else` (use explicit)
- `WPS334` — no reversed `while` condition
- `WPS335` — no `yield from` in async functions (use `async for`)
- `WPS336` — no explicit string concatenation
- `WPS337` — no multiline conditions with backslash
- `WPS338` — no useless node (empty `if`, `try`, etc.)
- `WPS339` — no pointless `continue` in `else`
- `WPS340` — no extra `+` in string
- `WPS341` — no `upper()` / `lower()` for comparison (use `.casefold()` or constant)
- `WPS342` — no `wraps()` usage without a callable
- `WPS343` — no direct `open()` — use `pathlib` or context manager
- `WPS344` — no `unreachable` code after `return`/`raise`
- `WPS345` — no `redundant` comparisons
- `WPS346` — no wrong list unpacking
- `WPS347` — no `from module import *`
- `WPS348` — no line starting with a dot
- `WPS349` — no redundant subscript slices
- `WPS350` — no augmented assignment (`+=`) for mutable objects in some contexts
- `WPS351` — no unnecessary literals (`list([])` → `[]`)
- `WPS352` — no multiline loop
- `WPS353` — no `map()`/`filter()` — use comprehensions
- `WPS354` — no consecutive `yield` expressions
- `WPS355` — no extra blank lines
- `WPS356` — no implicit item assignment in comprehension
- `WPS357` — no redundant `()`
- `WPS358` — no `0o` with uppercase `O`
- `WPS359` — no iterable unpacking in `return`
- `WPS360` — no unnecessary parentheses in `return`/`yield`/`assert`/`del`
- `WPS361` — no multiline comprehension
- `WPS362` — no walrus operator
- `WPS363` — no nested `f-string`
- `WPS364` — no redundant `elif` after `return`
- `WPS365` — no `return` with mutable containers
- `WPS366` — no `yield` from a lambda

## Key coding patterns

```python
# Names: descriptive, snake_case, no single-chars outside loops
user_count = 0
for index, user in enumerate(users):  # use enumerate, not range(len)
    ...

# Constants: UPPER_CASE at module level, immutable
MAX_RETRIES: Final = 3

# Imports: absolute only, grouped (stdlib, third-party, local)
from myapp.users import UserService  # not: from . import UserService

# Functions: small (<=20 lines), few args (<=5), single return type
def fetch_user(user_id: int) -> User:
    ...

# Classes: inherit explicitly (not `object`), use `@final` when not subclassed
@final
class UserRepository:
    ...

# Comparisons: use `is` for None/True/False
if result is None:
    ...
if items:  # not: if len(items) > 0
    ...

# Strings: f-strings preferred; no implicit concatenation; no % formatting
message = f'Hello {name}'

# Error handling: specific exceptions, not bare `except` or `except Exception`
try:
    result = fetch()
except RequestError as exc:
    raise ServiceError from exc
```

## Config awareness

Before writing or fixing code, check:
- `setup.cfg` / `.flake8` / `pyproject.toml [tool.flake8]` for overrides (`max-line-length`, `max-arguments`, `per-file-ignores`, `extend-exclude`, etc.)
- Inline `# noqa: WPSXXX` — respect existing ignores; do not remove them
- `per-file-ignores` — rules already silenced for a file do not need to be fixed

## MCP usage

When `flake8` reports a violation code `WPSXXX`:

```
# 1. Get explanation via MCP
explanation = explain_violation("WPSXXX")

# 2. Fix the code based on the explanation
# 3. Only if fix is impossible and user explicitly asked to ignore:
# add:  # noqa: WPSXXX
```
