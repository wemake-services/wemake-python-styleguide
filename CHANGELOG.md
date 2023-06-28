# Version history

We follow [Semantic Versions](https://semver.org/) since the `0.1.0` release.
We used to have incremental versioning before `0.1.0`.

Semantic versioning in our case means:
- Bugfixes do not bring new features, code that passes on `x.y.0`
  should pass on `x.y.1`.
  With the only exception that bugfix can raise old violations in new places,
  if they were hidden by a buggy behaviour. But we do not add new checks.
- Minor releases do bring new features and configuration options.
  New violations can be added. Code that passes on `x.0.y`
  might not pass on `x.1.y` release because of the new checks.
- Major releases inidicate significant milestones or serious breaking changes.
  There are no major releases right now: we are still at `0.x.y` version.
  But, in the future we might change the configuration names/logic,
  change the client facing API, change code conventions significantly, etc.

## WIP

### Bugfixes

- Fix `ForbiddenInlineIgnoreViolation` config parsing. #2590

## 0.18.0

### Features

- **Breaking**: drops `python3.7` support, because it has almost reached its EOL
- Adds `python3.11` support
- Bump `flake8` to version `5.x`
- Bump `flake8-*` dependencies to newer versions
- Added `ChainedIsViolation` #2443
- Added `BuggySuperContextViolation` #2310

### Bugfixes

- Make `generic_visit()` check script properly handle `with` statements.
- Allow calling magic methods with the same name as the enclosing method #2381
- Fix WrongEmptyLinesCountViolation false positive #2531
- Fix OpenWithoutContextManagerViolation false positive #2577

### Misc

- Replaced `flakehell` mentions to `flakeheaven` #2409


## 0.17.0

### Features

- **Breaking**: drops `python3.6` support
- Adds support for pattern matching naming rules, same as other variables
- Adds `--show-violation-links` option to show links to violation docs
- Adds `__init_subclass__` in the beginning of accepted methods
  order as per WPS338 #2411
- Adds `WrongEmptyLinesCountViolation` to check
  for too many lines in functions and methods definitions #2486

### Bugfixes

- Fixes `WPS226` false positives on `|` use in `SomeType | AnotherType`
  type hints syntax
- Now `-1` is not reported to be an overused expression
- Allow `__aiter__` to be async iterator
- Adds violation method name to error message of `YieldMagicMethodViolation`
- Fixes direct docker image invocation #2492

### Misc

- Adds full violation codes to docs and `BaseViolation.full_code` #2409
- Fix documentation mismatch between default setting
  for `max-string-usages` and enforced rule #2456
- Domain name was changed from `wemake-python-stylegui.de`
  to `wemake-python-styleguide.rtfd.io`


## 0.16.1

### Bugfixes

- Fixes crash on `'Literal["raise"]'` annotation #2341
- Fixes `WPS471` was not detected on complex assignment targets #2301
- Fixes `flake8-bandit` and `bandit` version conflict #2368


## 0.16.0

## Features

- Supports new `flake8` version `4.x`
- Now `InconsistentYieldViolation` and `InconsistentReturnViolation` are raised
  when `yield` or `return` is used with `None`
  where plain version should be used #2151
- Dot `'.'` and comma `','` do not count against string literal overuse limit anymore #2209
- Added `RedundantEnumerateViolation` #1825
- Adds `RaiseFromItselfViolation` #2133
- Adds `ConsecutiveSlicesViolation` #2064
- Adds `KwargsUnpackingInClassDefinitionViolation` #1754
- `DirectMagicAttributeAccessViolation` now only flags instances for which
  a known alternative exists #2268
- Forbids getting collection element of list by unpacking #1824
- Now `WPS227` forbids returning tuples that are too long #1731

### Bugfixes

- Fixes that `InconsistentComprehensionViolation` was ignoring
  misaligned `in` expressions #2075
- Fixes some common magic methods not being recognized as such #2281

### Misc

- Removes all `Raises:` from docstrings, they were unused
- Added example to `README.md`
- Added `why strict is good`
- Replaced all `python` with `Python` in `README.md`
- Improve Docs: Fixed all typos and grammatical errors in `CHANGELOG.md`
- Updated documentation with the recommended `isort` config. #1934
- Updates `typing_extensions` to `4.x`


## 0.15.3

### Bugfixes

- Fixes crash on `python3.10`
- Fixes `UselessReturningElseViolation` to not report `else` with `break` #1958
- Fixes `ReassigningVariableToItselfViolation` to not report on `x = (x,)` #1807
- Fixes `ReassigningVariableToItselfViolation` to extract variables
  from unary operators #1874
- Fixes that `f'{some:,}'` was considered too complex #1921
- Fixes that `range(len(x))` was not allowed even outside `for` loops #1883
- Fixes `UselessReturningElseViolation` to not report `else` with `break` #2187
  (even if we have `except` in loop)
- Fixes fixture in `UselessReturningElseViolation` #2191

### Misc

- Adds documentation (and tests) for how to run project on Jupyter Notebooks
- Updates `mypy` to `0.902` and fixes type issues


## 0.15.2

### Bugfixes

- Fixes `BitwiseAndBooleanMixupViolation` work with PEP 604 union types #1884
- Fixes `CognitiveModuleComplexityViolation` to not trigger
  for a single-item modules
- Fixes that `ConstantConditionViolation` was not reported for a `BoolOp`
- Functions and methods marked as `@overload` or `@typing.overload`
  do not count in complexity rules

### Misc

- Updates GitHub Action's base Python image version to `3.8.8`

### Features

- Adds a math operations evaluator to improve and allow several violation checks.


## 0.15.1

### Bugfixes

- Fixes `dataclasses` import, it was failing on `python3.6`
- Fixes `InconsistentComprehensionViolation` work with `async` comprehensions
- Fixes nested comprehensions support for `InconsistentComprehensionViolation`
- Fixes multiple `if` support for `InconsistentComprehensionViolation`
- Fixes that `NestedTernaryViolation` was not reported for a comprehension
- Fixes that `ConstantConditionViolation` was not reported for a comprehension
- Fixes that `ConstantConditionViolation` was triggering for `while x := True:`
- Fixes that `UselessElseViolation` was not reported
  for `for`, `while`, and `try` keywords
- Fixes false positive `InfiniteWhileLoopViolation` for `try` #1857
- Fixes that `InfiniteWhileLoopViolation` was not triggered on `1`
  or other truthy nodes

### Misc

- Refactors how `tokenize` tests are executed,
  now we have an option to compile fixture code
  to make sure it is syntactically valid.


## 0.15.0 aka python3.9

### Features

- Adds `python3.9` support
- Forbids to use new-style decorators on `python3.9`
- Changes how we treat own/foreign attributes,
  since now we only check assigned attribute names for `self`/`cls`/`mcs`,
  but not any other ones.
  So, now writing `point.x = 1` will not trigger any violations.
  Previously, it would raise "too short name".
- Forbids using non-trivial expressions as an argument to `except`
- Forbids using too many variables in a tuple unpacking
- Forbids using `float("NaN")`.
- Forbids assigning to a slice
- Allow `__call__` method to be asynchronous
- Allows common strings not to be counted against string constant overuse limit
- Forbids to unpack iterable objects to lists #1259
- Forbids to use single `return None`
- Add `__await__` to the list of priority magic methods
- Forbids to use float zeros (`0.0`)
- Forbids `raise Exception` and `raise BaseException`
- Forbids to use `%` with zero as the divisor
- Forbids testing conditions to just return booleans
  when it is possible to simply return the condition itself
- Forbids to use unsafe infinite loops
- Forbids to use raw strings `r''` when not necessary
- Forbids to use too complex `f`-strings
- Forbids to use too many `raise` statements inside a single function
- Forbids to compare with `float` and `complex` values
- Forbids single element destruct
- Forbids to ignore some violations (configurable) on a line level
- Forbids single element unpacking
- Forbids to unpack lists with side-effects
- Forbids to use multiline strings except for assignments and docstrings
- Forbids not returning anything in functions and methods starting with `get_`
- Forbids to use empty comment
- Forbids using bitwise operation with boolean operation
- Forbids inconsistent structuring of multiline comprehensions
- Forbids to use unpythonic getters and setters such as `get_attribute` or `set_attribute`
- Now `credits`, `license`, and `copyright` builtins are free to shadow

### Bugfixes

- Fixes fails of annotation complexity on `Literal[""]`
- Fixes how wrong variable names were checked case sensitive with `WPS110`
- Fixes false positives DirectMagicAttributeAccessViolation with `__mro__`, `__subclasses__` and `__version__`
- Make `WPS326` work when there is comment between string literals
- Allowed yield statements in call method
- Allow to use `^` with `1`
- Fixes false positives in WPS513 and WPS323
- Fixes false positive WPS426 if `lambda` in loop uses only its arguments
- Fixes false negative WPS421 with `pprint.pprint`
- Fixes WPS441 triggering when reusing variable names in multiple loops
- Fixes false positive ImplicitEnumerateViolation on range with step #1742
- Allows to use `_` to declare several unused variables,
  like: `x, _, _ = coordinates()`
- Fixes variable reassignment in class context
- Fixes that `*'abc'` was not counted as pointless star expression
- Fixes that `-some` was counted as overused expression
- Fixes several bugs with attribute names

### Misc

- Updates lots of dependenices
- Fixed documentation for TooManyPublicAttributesViolation
- Updated isort config
- Introduce helper script to check
  for missing calls to `self.generic_visit(node)` in AST visitors
- Updates `poetry` version to `1.1`
- Updates `reviewdog` version to `0.11.0` and adds `action-depup`


## 0.14.0 aka The Walrus fighter

This release was focused on adding `python3.8` support,
removing dependencies that can be removed, and fixing bugs.

There are breaking changes ahead!

We also have this [nice 0.14 migration guide](https://wemake-python-styleguide.rtfd.io/en/latest/pages/changelog/migration_to_0_14.html).

### Features

- **Breaking**: removes `flake8-executable`, now using `WPS452` instead of `EXE001..EXE005`
- **Breaking**: removes `flake8-print`, now using `WPS421` instead of `T001`
- **Breaking**: removes `flake8-builtins`, now using `WPS125` instead of `A001..A005`
- **Breaking**: removes `flake8-annotations-complexity`,
  now using `WPS234` instead of `TAE002`
- **Breaking**: removes `flake8-pep3101`, now using `WPS323` instead of `S001`,
  we also use a new logic for this violation:
  we check string defs for `%` patterns, and not for `%` operator
- **Breaking**: `WPS441` is no longer triggered for `except` blocks,
  it is now handled by `F821` from `flake8`
- **Breaking**: removes `radon`,
  because `cognitive-complexity` and `mccabe` is enough
- **Breaking**: removes `flake8-logging-format` as a direct dependency
- **Breaking**: removes `ImplicitTernaryViolation` or `WPS332`,
  because it has too many false positives #1099
- Removes `flake8-coding`, all encoding strings, visitor and tests
  for old `WPS323` which is now reused for modulo formatting checks
- Adds `python3.8` support
- Changes `styleguide.toml` and `flake8.toml` scripts definition
- Extracts new violation - `WPS450` from `WPS436` #1118
- Adds domain names options:
  `--allowed-domain-names` and `--forbidden-domain-names`,
  that are used to create variable names' blacklist #1106
- Forbids to use `\r` (carriage return) as line breaks in strings #1111
- Forbids to use `:=` operator, it now reuses `WPS332` code
- Forbids to use positional only `/` arguments
- Forbids to have too many names imported from a single `from ... import`
- Forbids to use `continue` and `break` in `finally`
- Forbids to use `__reduce__` and `__reduce_ex__` magic methods
- Adds `__call__` to list of methods that should be on top #1125
- Allows `_` to be now used as a defined variable
- Removes `cognitive_complexity` dependency, now it is built in into our linter
- Adds baseline information for all complexity violation messages: `x > baseline`
- Changes how cognitive complexity is calculated
- Adds support for positional arguments in different checks
- Adds `UnreadableNameViolation` as `WPS124` because there are some
character combination which is not easy to read
- Adds support for `NamedExpr` with in compare type violation
- Forbids `float` and `complex` compares

### Bugfixes

- Fixes how `i_control_code` behaves with `WPS113`
- Fixes that cognitive complexity was ignoring
  `ast.Continue`, `ast.Break`, and `ast.Raise` statements
- Fixes that cognitive complexity was ignoring `ast.AsyncFor` loops
- Fixes that annotation complexity was not reported for `async` functions
- Fixes that annotation complexity was not reported for lists
- Fixes that annotation complexity was not reported for `*` and `/` args
- Fixes that annotation complexity was not tested for dot notation attributes
- Fixes that annotation complexity fails on string expressions
- Fixes bug when `TooManyPublicAttributesViolation`
  was counting duplicate fields
- Fixes negated conditions `WPS504` was not reported for `if` expressions
- Fixes that `import dumps` was reported as `WPS347`,
  now only `from ... import dumps` is checked
- Fixes that `from some import a as std` was reported as a vague import
  with `WPS347` despite having a meaningful alias
- Fixes that `WPS501` was reported for `@contextmanager` definition
- Fixes `WPS226` to be thrown at nested string type annotations
- Fixes `WPS204` reported simplest nodes as overused like `[]` and `call()`
- Fixes `WPS204` not reporting overused `f` strings
- Fixes `WPS204` reporting overused return type annotations
- Fixes `WPS204` reporting `self.` attribute access
- Fixes `WPS331` reporting cases that do require some extra steps before return
- Fixes `WPS612` not reporting `super()` calls without return
- Fixes `WPS404` not raising on wrong `*` and `/` defaults
- Fixes `WPS425` raising on `.get`, `getattr`, `setattr`,
  and other builtin functions without keyword arguments
- Fixes `WPS221` reporting differently on different `python` versions
- Fixes `WPS221` reporting nested variable annotations
- Fixes `WPS509` not reporting nested ternary in grandchildren of `if`
- Fixes `WPS509` not reporting nested ternary in ternary
- Fixes `WPS426` not reporting nested `lambda` in comprehensions
- Fixes several violations to reporting for `ast.Bytes` and `ast.FormattedStr`
  where `ast.Str` was checked
- Fixes `WPS601` reporting shadowing for non-`self` attributes
- Fixes `WPS114` not to be so strict
- Fixes `WPS122` not raising for `for` and `async for` definitions
- Fixes `WPS400` raising for `# type: ignore[override]` comments
- Fixes `WPS115` not raising for attributes inside other nodes

### Misc

- Changes how tests are executed
- Changes how coverage is calculated, adds `coverage-conditional-plugin`
- Adds how a violation can be deprecated
- Improves old visitor tests with `/` argument cases
- Improves old visitor tests with `:=` cases
- Adds `local-partial-types` to mypy config
- Uses `abc` stdlib's module to mark abstract base classes #1122
- Adds `python3.8` to the CI
- Updates a lot of dependencies


## 0.13.4

This is the last `0.13.x` supporting release,
we have to concentrate on `python3.8` support
and `0.14.0` which will introduce it to the public.

### Bugfixes

- Fix false positive ImplicitYieldFromViolation for async functions #1057
- Fixes nested-classes-whitelist option default value for flake8 prior 3.7.8 #1093
- Improve boolean non-keyword arguments validation #1114

### Misc

- Updates `flake8-pep3101`
- Updates `flake8-builtins`
- Updates `flake8-eradicate`
- Several small refactoring sessions
- Adds `hypothesis`-based tests
- Adds `flakehell` base config
- Fixes `flakehell` docs
- Fixes `MAX_NOQA_COMMENTS` and related violation docs
- Fixes `OverusedExpressionViolation` and `TooManyExpressionsViolation` docs


## 0.13.3

### Misc

- Updates `radon` version
- Updates `poetry` version to `1.0`


## 0.13.2

### Bugfixes

- Fixes that Github Action was failing for wrong status code
- Fixes `NegatedConditionsViolation` false positive on absent
  `else` in combination with `elif`
- Fixes `WPS528` false positive on augmented assigns
- Fixes incorrect message for `WPS349`
- Fixes that `reviewdog` was not able to create more than `30` comments per PR

### Misc

- `pylint` docs fixed
- Fixes docs about implicit `yield` violation


## 0.13.1

### Bufixes

- Fixes that `_` was marked as invalid by `VagueImportViolation`
- Fixes that docs for `VagueImportViolation` were misleading
- Fixes invalid docs for `BracketBlankLineViolation` #1020
- Add more complex example to `ParametersIndentationViolation` #1021

### Misc

- Now our GitHub Action can be used to leave PR review comments


## 0.13.0 aka The Lintoberfest

This is a huge release that was created during the Hactoberfest season.
It was impossible without the huge help from [our awesome contributors](https://github.com/wemake-services/wemake-python-styleguide/graphs/contributors?from=2019-06-01&to=2019-11-18&type=c). Thanks a lot to everyone!

This release is not focused on any particular area.
It features a lot of new rules from different categories.

### Features

- Adds cognitive complexity metric, introduced by [`cognitive_complexity`](https://github.com/Melevir/cognitive_complexity)
- Adds docstrings linter [`darglint`](https://github.com/terrencepreilly/darglint)
- Updates `pep8-naming` and `flake8-comprehensions`
- `WPS431` now allow customize whitelist via `nested-classes-whitelist` setting
- Forbids to have invalid strings in stared expressions like `**{'@': 1}`
- Forbids to use implicit primitive values in a form of `lambda: 0`
- Forbids to use approximate math constants
- Forbids to redefine string constants
- Forbids use of vague import names (e.g. `from json import loads`)
- Makes `OveruseOfNoqaCommentViolation` configurable via `--max-noqa-comments`
- Forbid incorrectly swapped variables
- Forbids to use redundant subscripts (e.g., `[0:7]` or `[3:None]`)
- Allows `super()` as a valid overused expression
- Forbids to use `super()` with other methods and properties
- `WPS350` enforces using augmented assign pattern
- Forbids unnecessary literals
- `WPS525` forbids comparisons where `in` is compared with single item container
- Forbids wrong annotations in assignment
- Forbids using multiline `for` and `while` statements
- `WPS113` now can be tweaked with `I_CONTROL_CODE` setting
- Adds `WPS000` that indicates internal errors
- Forbids to use implicit `yield from`
- Forbids to start lines with `.`
- Enforces better `&`, `|`, `>>`, `<<`, `^` operators usage
- Forbids incorrect exception order
- Enforces tuples usage with frozenset constructor
- Changes how `WPS444` works, now we use stricter logic for `while` and `assert`
- Forbids to use `yield from` with incorrect types
- Forbids to use consecutive `yield` expressions
- Enforces to use `.items()` in loops
- Enforces using `.get()` over `key in dict` checks
- Forbids to use and declare `float` keys in arrays and dictionaries
- Forbids to use `a[len(a) - 1]` because it is just `a[-1]`
- Forbids too long call chains like `foo(a)(b)(c)(d)`

### Bugfixes

- Fixes `ImplicitElifViolation` false positives on a specific edge cases
- Fixes `--i-control-code` setting for `BadMagicModuleFunctionViolation`
- Fixes compatibility with flake8 `3.8.x`
- Fixes that `not not True` was not detected as `WPS330`
- Fixes addition of `MisrefactoredAssignmentViolation` check
- Fixes `WrongMagicCommentViolation` not catching certain wrong comments
- Fixes `BadMagicModuleFunctionViolation` false positives on class-level methods
- Fixes `InconsistentReturnViolation` false positives on nested functions
- Fixes that `--i-dont-control-code` was not present in command line options
- Fixes `BlockVariableVisitor` false positives on a properties
- Fixes that `//` was not recognised as a math operation
- Fixes false positive `BlockAndLocalOverlapViolation` on annotations without value assign
- Fixes bug when `x and not x` was not detected as the similar conditions by `WPS408`
- Fixed that `1.0` and `0.1` were treated as magic numbers

### Misc

- Improves Github Action stability
- Replace `scripts/tokens.py` and `scripts/parse.py` with external tools
- Improves violation code testing
- Improves testing of `.. versionchanged` and `previous_codes` properties
- Reference `isort` settings requirement for compliance with `WSP318` in docstring
- Improves tests: we now ensure that each violation with previous codes also
  has corresponding versions changed in their documentation


## 0.12.5

### Bugfixes

- We now ignore `@overload` from `BlockAndLocalOverlapViolation`
- Now expressions that reuse block variables are not treated as violations,
  example: `my_var = do_some(my_var)`

### Misc

- Adds Github Action and docs how to use it
- Adds local Github Action that uses itself for testing
- Adds official Docker image and docs about it


## 0.12.4

### Bugfixes

- Fixes bug with `nitpick` colors and new files API
- Updates `flake8-docstrings`


## 0.12.3

### Bugfixes

- Fixes that formatting was failing sometimes when colours were not available
- Fixes that `1 / number` was not allowed
- Fixes that `%` operator was allowed for `0` and `1`


## 0.12.2

### Features

- Adds `reveal_type` to the list of forbidden functions
- `WPS517` now allows to use non-string keys inside `**{}`,
  so this is allowed: `Users.objects.get(**{User.USERNAME_FIELD: username})`

### Bugfixes

- Fixes that `{**a, **b}` was reported as duplicate hash items


## 0.12.1

### Features

- Tweaks `nitpick` configuration

### Bugfixes

- Changes `radon` and `pydocstyle` versions for better resolution
- Fixes `nitpick` urls

### Misc

- Improves `README.md` with `flakehell` and `nitpick` mentions
- Improves docs all across the project


## 0.12.0

In this release we had a little focus on:

0. Primitives and constants and how to use them
1. Strings and numbers and how to write them
1. OOP features
1. Blocks and code structure,
   including variable scoping and overlapping variables
1. Overused expressions and new complexity metrics

### Features

- **Breaking**: moves `ImplicitInConditionViolation` from `WPS336` to `WPS514`
- **Breaking**: now `ExplicitStringConcatViolation` uses `WPS336`
- **Breaking**: moves `YieldMagicMethodViolation` from `WPS435` to `WPS611`
- Adds `xenon` as a dependency, it also checks for cyclomatic complexity,
  but uses more advanced algorithm with better results
- Forbids to have modules with too many imported names
  configured by `--max-imported-names` option which is 50 by default
- Forbids to raise `StopIteration` inside generators
- Forbids to have incorrect method order inside classes
- Forbids to make some magic methods async
- Forbids to use meaningless zeros in float, binary, octal, hex,
  and expanentional numbers
- Enforces to use `1e10` instead of `1e+10`
- Enforces to use big letters for hex numbers: `0xAB` instead of `0xab`
- Enforces to use `r'\n'` instead of `'\\n'`
- Forbids to have unicode escape characters inside binary strings
- Forbids to use `else if` instead of `elif`
- Forbids to have too long `try` bodies,
  basically `try` bodies with more than one statement
- Forbids to overlap local and block variables
- Forbids to use block variables after the block definitions
- Changes how `WrongSlotsViolation` works, now `(...) + value` is restricted
  in favor of `(..., *value)`
- Forbids to have explicit unhashable types in sets and dicts
- Forbids to define useless overwritten methods
- Enforces `j` prefix over `J` for `complex` numbers
- Forbids overused expressions
- Forbids explicit `0` division, multiply, pow, addition, and subtraction
- Fordids to pow, multiply, or divide by `1`
- Forbids to use expressions like `x + -2`, or `y - -1`, or `z -= -1`
- Forbids to multiply lists like `[0] * 2`
- Forbids to use variable names like `__` and `_____`
- Forbids to define unused variables explicitly: `_unused = 2`
- Forbids to shadow outer scope variables with local ones
- Forbids to have too many `assert` statements in a function
- Forbids to have explicit string contact: `'a' + some_data`, use `.format()`
- Now `YieldInsideInitViolation` is named `YieldMagicMethodViolation`
  and it also checks different magic methods in a class
- Forbids to use `assert False` and other false-constants
- Forbids to use `while False:` and other false-constants
- Forbids to use `open()` outside of `with`
- Forbids to use `type()` for compares
- Forbids to have consecutive expressions with too deep access level
- Forbids to have too many public instance attributes
- Forbids to use pointless star operations: `print(*[])`
- Forbids to use `range(len(some))`, use `enumerate(some)` instead
- Forbids to use implicit `sum()` calls and replace them with loops
- Forbids to compare with the falsy constants like `if some == []:`

### Bugfixes

- Bumps `flake8-eradicate` version
  and solves `attrs` incompatible versions issue
- Bumps `flake8-dosctrings` version
  and solved `pydocstyle` issue
- Fixes `TryExceptMultipleReturnPathViolation` not tracking `else` and `finally`
  returns at the same time
- Fixes how `TryExceptMultipleReturnPathViolation` works:
  now handles `break` and `raise` statements as well
- Fixes `WrongLoopIterTypeViolation` not triggering
  for generator expressions and empty tuples
- Fixes `WrongLoopIterTypeViolation` not triggering
  for numbers (including negative), booleans, `None`
- Fixes `WrongLoopIterTypeViolation` position
- Fixes `WrongLoopIterTypeViolation` not triggering for compehensions
- Fixes `WrongSlotsViolation` not triggering
  for comprehensions and incorrect `__slots__` names and types
- Fixes `WrongSlotsViolation` not triggering
  for invalid `python` identifiers like `__slots__ = ('123_slot',)`
- Fixes `WrongSlotsViolation` triggering for subscripts
- Fixes `NestedClassViolation` and `NestedFunctionViolation` not reporting
  when placed deeply inside other nodes
- Fixes when `WrongUnpackingViolation` was not raised
  for `async for` and `async with` nodes
- Fixes when `WrongUnpackingViolation` was not raised for comprehensions
- Fixes that `x, y, z = x, z, y` was not recognized
  as `ReassigningVariableToItselfViolation`
- Fixes that `{1, True, 1.0}` was not recognised as a set with duplicates
- Fixes that `{(1, 2), (1, 2)}` was not recognised as a set with duplicates
- Fixes that `{*(1, 2), *(1, 2)}` was not recognised as a set with duplicates
- Fixes that `{1: 1, True: 1}` was not recognised as a dict with duplicates
- Fixes that `complex` numbers were always treated like magic,
  now `1j` is allowed
- Fixes that `0.0` was treated as a magic number
- Fixes that it was possible to use `_` in module body
- Fixes `WrongBaseClassViolation` not triggering
  for nested nodes like `class Test(call().length):`
- Fixes `ComplexDefaultValueViolation` not triggering
  for nested nodes like `def func(arg=call().attr)`
- Fixes `TooShortNameViolation` was not triggering for `_x` and `x_`
- Fixes that some magic method were allowed to be generators
- Fixes that some magic method were allowed to contain `yield from`
- Fixes bug when some correct `noqa:` comments were reported as incorrect
- Fixes bug when some `else: return` were not reported as incorrect
- Fixes bug when `WPS507` sometimes were raising `ValueError`
- Fixes bug when `return None` was not recognized as inconsistent

### Misc

- Adds `styles/` directory with style presets for tools we use and recommend
- Adds `bellybutton` to the list of other linters
- Documents how to use `nitpick` to sync the configuration
- Documents how to use `flakehell` to create `baseline`s for legacy integrations
- Improves tests for binary, octal, hex, and exponentional numbers
- Adds new `xenon` CI check
- Now handles exceptions in our own code, hope to never see them!
- Now uses `coverage` checks in deepsource
- Now `@alias` checks that all aliases are valid
- Changes how presets are defined
- Improves how `DirectMagicAttributeAccessViolation` is tested
- Refactors a lot of tests to tests `ast.Starred`
- Refactors a lot of tests to have less tests with the same logical coverage
- We now use `import-linter` instead of `layer-linter`
- Adds docs about CI integration
- Now wheels are not universal
- Updates docs about `snake_case` in `Enum` fields
- Updates docs about `WPS400` and incorrect line number


## 0.11.1

### Bugfixes

- Now using `pygments` as a direct dependency


## 0.11.0 aka The New Violation Codes

We had a really big problem: all violations inside `best_practices`
was messed up together with no clear structure.

We had to fix it before it is too late.
So, we broke existing error codes.
And now we can promise not to do it ever again.

We also have this [nice 0.11 migration guide](https://wemake-python-styleguide.rtfd.io/en/latest/pages/changelog/migration_to_0_11.html)
for you to rename your violations with a script.

### Features

- **Breaking**: replaces `Z` error code to `WPS` code
- **Breaking**: creates new violation group `refactoring.py`
- **Breaking**: creates new violation group `oop.py`
- **Breaking**: moving a lot of violations
  from `best_practices` to `refactoring`, `oop`, and `consistency`
- Adds new `wemake` formatter (using it now by default)

### Bugfixes

- Fixes error message of `OverusedStringViolation` for empty strings
- Now does not count string annotations as strings for `OverusedStringViolation`
- Fixes `InconsistentReturnVariableViolation` was raised twice

### Misc

- Adds migration guide to `0.11`
- Improves legacy guide
- Adds `--show-source` to the default recommended configuration
- Adds better docs about auto-formatters
- Adds `autopep8` to CI to make sure that `wps` is compatible with it
- Ensures that `--diff` mode works for `flake8`
- Renames `Incorrect` to `Wrong` where possible
- Renames `IncorrectlyNestedTernaryViolation` to `NestedTernaryViolation`
- Renames `IncorectLoopIterTypeViolation` to `WrongLoopIterTypeViolation`


## 0.10.0 aka The Great Compare

This release is mostly targeted at writing better compares and conditions.
We introduce a lot of new rules related to this topic improving:
consistency, complexity, and general feel from your code.

In this release we have ported a lot of existing `pylint` rules,
big kudos to the developers of this wonderful tool.

### Features

- Adds `flake8-executable` as a dependency
- Adds `flake8-rst-docstrings` as a dependency
- Validates options that are passed with `flake8`
- Forbids to use module level mutable constants
- Forbids to over-use strings
- Forbids to use `breakpoint` function
- Limits yield tuple lengths
- Forbids to have too many `await` statements
- Forbids to subclass lowercase `builtins`
- Forbids to have useless `lambda`s
- Forbids to use `len(sized) > 0` and `if len(sized)` style checks
- Forbids to use repeatable conditions: `flag or flag`
- Forbids to write conditions like `not some > 1`
- Forbids to use heterogeneous compares like `x == x > 0`
- Forbids to use complex compare with several items (`>= 3`)
- Forbids to have class variables that are shadowed by instance variables
- Forbids to use ternary expressions inside `if` conditions
- Forces to use ternary instead of `... and ... or ...` expression
- Forces to use `c < b < a` instead of `a > b and b > c`
- Forces to use `c < b < a` instead of `a > b > c`
- Forbids to use explicit `in []` and `in ()`, use sets or variables instead
- Forces to write `isinstance(some, (A, B))`
  instead of `isinstance(some, A) or isinstance(some, B)`
- Forbids to use `isinstance(some (A,))`
- Forces to merge `a == b or a == c` into `a in {b, c}` and
  to merge `a != b and a != c` into `a not in {b, c}`

### Bugfixes

- Fixes incorrect line number for `Z331`
- Fixes that `Z311` was not raising for multiple `not in` cases
- Fixes a bunch of bugs for rules working with `Assign` and not `AnnAssign`
- Fixes that `continue` was not triggering `UselessReturningElseViolation`

### Misc

- Renames `logics/` to `logic/` since it is grammatically correct
- Renames `Redundant` to `Useless`
- Renames `Comparison` to `Compare`
- Renames `WrongConditionalViolation` to `ConstantConditionViolation`
- Renames `ComplexDefaultValuesViolation` to `ComplexDefaultValueViolation`
- Refactors `UselessOperatorsVisitor`
- Adds `compat/` package, getting ready for `python3.8`
- Adds `Makefile`
- A lot of minor dependency updates


## 0.9.1

### Bugfixes

- Fixes issue with `pydocstyle>=4` by glueing its version to `pydocstyle<4`


## 0.9.0

This is mostly a supporting release with several new features
and lots of bug fixes.

### Features

- Forbids to use magic module methods `__getattr__` and `__dir__`
- Forbids to use multiline conditions
- Forbids local variables that are only used in `return` statements

### Bugfixes

- Fixes module names for modules like `io.py`
- Fixes false positive `Z310` for numbers like `0xE`
- Fixes false positive for compare ordering with `await`
- Fixes problem with missing `_allowed_left_nodes`
- Fixes problem false positive for `Z121` when using `_` for unused var names
- Fixes false positive for negative number in default values
- Fixes error text for `ComplexDefaultValueViolation`
- Fixes problem with false positive for `Z459`
  when a default value is an `Ellipsis`

### Misc

- Adds `py.typed` file in case someone will import our code,
  now it will have types
- Adds several missing `@final` decorators
- Enforces typing support
- Refactors how `typing_extensions` package is used
- Adds docs about `black`
- Adds big "Star" button
- Multiple dependencies update
- Better `exclude` rule for `flake8` check
- Removed warnings from `pytest`


## 0.8.1

### Bugfixes

- Fixes how `wps_context` is calculated, so `super()` calls are now working


## 0.8.0

### Features

- Updates `flake8` to `3.7+`
- Adds `flake8-annotations-complexity` as a dependency, forbids complex annotations
- Forbids to use redundant `+`, `~`, `not`, and `-` operators before numbers
- Forbids to use complex default values
- Forbids to use anything rather than names in `for` loop vars definitions
- Forbids to use anything rather than names in `with` block vars definitions
- Forbids to use anything rather than names in comprehension vars definitions
- Forbids to use direct magic attributes access
- Forbids to use negated conditions
- Forbids to use too many `# pragma: no cover` comments
- Forbids to use nested `try` blocks

### Bugfixes

- Fixes problems with empty lines after magic comments, see [#492](https://github.com/wemake-services/wemake-python-styleguide/issues/492)
- Fixes error message for `del` keyword: it is now just `'del'` not `'delete'`

### Misc

- Removes `flake8-per-file-ignores` plugin, since `flake8` now handles it
- Removes `flake8-type-annotations` plugin, since `flake8` now handles it
- Improves docs for `WrongKeywordViolation`
- Improves docs for `EmptyLineAfterCodingViolation`
- Improves docs for `ProtectedAttributeViolation`
- Adds docs about `.pyi` files


## 0.7.1

### Bugfixes

- Allows `Generic[SomeType]` to be a valid superclass
- Forces to use `flake8` version `3.6` instead of `3.7`

### Misc

- Improves docs about using `# type: some` comment in `for` loops


## 0.7.0

### Features

- Now raising a violation for every `bool` non-keyword argument
  and showing better error message
- Changes how `max-arguments` are counted
  Now `self`, `cls`, and `mcs` count as real arguments
- Forbids to use `yield` inside comprehensions
- Forbids to have single line triple-quoted string assignments
- Forbids to have same items in `set` literals
- Forbids to subclass `BaseException`
- Forbids to use simplifiable `if` expressions and nodes
- Forbids to have incorrect nodes in `class` body
- Forbids to have methods without any arguments
- Forbids to have incorrect base classes nodes
- Enforces consistent `__slots__` syntax
- Forbids to use names with trailing `_` without a reason
- Forbids to use `super()` with arguments or outside of methods
- Forbids to have too many `except` cases
- Enforces to have an empty line after `coding` comment
- Forbids to use too many `# noqa` comments
- Forbids to use variables declared as unused
- Forbids to use redundant `else` blocks
- Forbids to use inconsistent `return` and `yield` statements
- Forbids to use multiple `return` path in `try`/`expect`/`finally`
- Forbids to use implicit string concatenation
- Forbids to have useless `continue` nodes inside the loops
- Forbids to have useless nodes
- Forbids to have useless `raise` statements
- Adds `params` and `parameters` to black-listed names

### Bugfixes

- Fixes a lot of rules that were ignoring `Bytes` node as constant type
- Fixes location of the `BooleanPositionalArgumentViolation`
- Fixes argument count issue with `async` functions
- Fixes `WrongConditionalVisitor` not detecting `tuple` as constants
- Fixes `WrongConditionalVisitor` not detecting negative numbers as constants
- Fixes some magic number that were not detected based on their location
- Fixes error when regular functions named as blacklisted
  magic methods were forbidden, now we check for methods only
- Fixes error when strings like `U'some'` was not triggering unicode violation
- Fixes error when string like `U'some'` was not triggering modifier violation

### Misc

- Adds `safety` and other dependency checks to the CI process
- Improves tests: now `tokenize` works differently inside tests
- Improves tests: now testing more brackets cases aka "magic coverage bug"
- Improves docs: adds new badge about our code style
- Refactoring: trying to use `astor` where possible to simplify the codebase
- Refactoring: introduces some new `transformations`
- Refactoring: now we do not have any magical text casts for violations
- Improves tests: changes how `flake8` is executed, now it is twice as fast
- Improves docs: now linting `conf.py` with `flake8`
- Improves tests: now we check that ignored violation are raised with `noqa`
- Improves docs: we have added a special graph to show our architecture
- Improves docs: we now have a clean page for `checker` without extra junk
- Improves docs: we now have a tutorial for creating new rules
- Refactoring: moves `presets` package to the root
- Improves tests: we now lint our layered architecture with `layer-lint`


## Version 0.6.3

### Bugfixes

- Fixes an [issue-450](https://github.com/wemake-services/wemake-python-styleguide/issues/450) with `dict`s with just values and no keys


## Version 0.6.2

### Bugfixes

- Fixes a [crash](https://github.com/wemake-services/wemake-python-styleguide/issues/423) with class attributes assignment


## Version 0.6.1

### Bugfixes

- Fixes a conflict between our plugin and `pyflakes`


## Version 0.6.0

### Features

- Adds `flake8-per-file-ignore` plugin dependency
- Adds default values to the `flake8 --help` output
- Adds `do` as a restricted variable name
- Forbids multiple assignment targets for context managers
- Forbids to use incorrect multi-line parameters
- Forbids to use `bool` values as positional arguments
- Forbids to use extra indentation
- Forbids to use inconsistent brackets
- Forbids to use multi-line function type annotations
- Forbids to use uppercase string modifiers
- Forbids to use assign chains: now we only can use one assign per line
- Forbids to use assign with unpacking for any nodes except `Name`
- Forbids to have duplicate `except` blocks

### Bugfixes

- Fixes tests failing on windows (@sobolevn hates windows!),
  but it still fails sometimes
- Fixes bug when `@staticmethod` was treated as a module member
- Fixes bug when some nodes were not checked with `TooDeepNestingViolation`
- Fixes bug when it was possible to provide non-unique aliases
- Fixes incorrect line number for incorrect parameter names
- Fixes bug when names like `__some__value__` were not treated as underscored
- Fixes bug when assignment to anything rather than name was raising an error

### Misc

- Refactoring: now we fix `async` nodes offset in a special transformation
- Improves docs: specifies what `transformation` is
- Improves docs: making contributing section in the `README` more friendly
- Improves build: changes how CI installs `poetry`


## 0.5.1

### Bugfixes

- Fixes all possible errors that happen
  because of unset `parent` and `function_type` properties


## 0.5.0

### Features

- **Breaking**: removes `--max-conditions` and `--max-elifs` options
- **Breaking**: removes `--max-offset-blocks`
- **Breaking**: changes default `TooManyConditionsViolation` threshold from `3` to `4`
- **Breaking**: changes `TooManyBaseClassesViolation` code from `225` to `215`
- Forbids to use `lambda` inside loops
- Forbids to use `self`, `cls`, and `mcs` except for first arguments only
- Forbids to use too many decorators
- Forbids to have unreachable code
- Forbids to have statements that have no effect
- Forbids to have too long names for modules and variables
- Forbids to have names with unicode for modules and variables
- Add `variable` to the blacklisted names
- Now `RedundantLoopElseViolation` also checks `while` loops

### Bugfixes

- Fixes `TooManyConditionsViolation` to work with any conditions, not just `if`s
- Fixes `TooManyConditionsViolation` that did not count conditions correctly
- Fixes `TooManyForsInComprehensionViolation` to find all comprehension types
- Fixes `TooManyElifsViolation` to check module level conditions
- Fixes `TooManyBaseClassesViolation` docs location
- Fixes `WrongVariableNameViolation` not checking `lambda` argument names
- Fixes `OffsetVisitor` incorrect `await` handling

### Misc

- Refactoring: moves all complexity checks into `complexity/` folder
- Refactoring: improves how different keyword visitors are coupled
- Improves docs: we have removed magic comments and code duplication
- Improves docs: now `_pages/` is named just `pages/`
- Improves docs: now all violations are sorted correctly
- Improves tests: now testing different keywords separately
- Improves tests: now all violations must be contained in `test_noqa.py`
- Improves tests: now we also run `compile()` on all `ast` examples
- Improves tests: now we are sure about correct order of violations

## 0.4.0

Development was focused around better test coverage and providing a better API
for tests. We also now covering more cases and testing violation texts.

### Features

- **Breaking**: removes duplicating module name rules, now we use the same rules
  for both variables and modules
- **Breaking**: removes `--min-module-name-length` options
- **Breaking**: renames `--min-variable-name-length` into `--min-name-length`
- Dependencies: updates `flake8` version to `3.6`
- Dependencies: removes `pycodestyle` pinned version
- Restrict unicode names

### Bugfixes

- Multiple fixes to error text formats to be more readable
- Fixes `UNDERSCORED_NUMBER_PATTERN` to match names like `come_22_me`
- Fixes `UpperCaseAttributeViolation` not being displayed in the docs
- Fixes consistency checks being duplicated in the docs
- Fixes `UnderscoredNumberNameViolation` showing incorrect line number
- Fixes `ProtectedAttributeViolation` to respect `super()` and `mcs`
- Fixes `ProtectedAttributeViolation` to show correct text
- Fixes `BadNumberSuffixViolation` to show correct text
- Fixes `TooManyBaseClassesViolation` to show correct text
- Fixes `TooManyElifsViolation` to show correct text
- Fixes `TooDeepNestingViolation` to show correct text
- Fixes `TooManyMethodsViolation` to show correct text
- Fixes `ReassigningVariableToItselfViolation` to show correct text
- Renames `UnderscoredNumberNameViolation` to `UnderscoredNumberNameViolation`

### Misc

- Refactoring: removed duplicate logic inside `logics/filenames.py`
- Improves tests: now testing almost all violations inside `noqa.py`
- Improves tests: now testing violations text
- Improves tests: now all common patters live in related `conftest.py`
- Improves docs: now all configuration options are listed in the violations


## 0.3.0 aka The Hacktoberfest Feast

This release was made possible by awesome people who contributed
to the project during `#hactoberfest`. List of awesome people:

- [@novikovfred](https://github.com/novikovfred)
- [@riyasyash](https://github.com/riyasyash)
- [@sathwikmatsa](https://github.com/sathwikmatsa)
- [@tipabu](https://github.com/tipabu)
- [@roxe322](https://github.com/roxe322)
- [@geoc0ld](https://github.com/geoc0ld)
- [@lensvol](https://github.com/lensvol)
- [@SheldonNunes](https://github.com/SheldonNunes)
- [@tommbee](https://github.com/tommbee)
- [@valignatev](https://github.com/valignatev)
- [@vsmaxim](https://github.com/vsmaxim)

### Features

- Adds `flake8-print` as a dependency
- Adds `typing-extensions` as a dependency
- Forbids to use `quit` and `exit` functions
- Forbids the comparison of two literals
- Forbids the incorrect order comparison, enforcing variable to come first
- Forbids underscores before numbers in names
- Forbids class level attributes whose name is not in `snake_case`
- Forbids comparison of the same variables
- Forbids inconsistent octal, binary, and hex numbers
- Forbids too many arguments in `lambda` functions
- Forbids extra `object` in parent classes list
- Forbids `for` loops with unused `else`
- Forbids variables self reassignment
- Forbids `try` with `finally` without `except`
- Forbids `if` statements with invalid conditionals
- Forbids opening parenthesis from following keyword without space in between them
- Forbids the use of more than 2 `for` loops within a comprehension
- Forbids variable names with more than one consecutive underscore
- Restricts the maximum number of base classes aka mixins
- Forbids importing protected names
- Forbids using protected methods and attributes
- Forbids `yield` inside `__init__` method

### Bugfixes

- Fixes that `MultipleIfsInComprehensionViolation` was not enabled
- Fixes flaky behaviour of `test_module_names` test package
- Fixed `TooManyMethodsViolation` not displaying line number in output
- Fixed `OffsetVisitor` due to python [bug](https://bugs.python.org/issue29205)

### Misc

- Updates `poetry` version
- Refactoring: some general changes, including better names and APIs
- Improves docs: now we have `versionadded` for each violation
- Improves docs: now we explicitly state how some violations might be ignored
- Improves tests: now we are testing options
- Improves tests: now we have different `tests/` folder structure
- Improves tests: now we are testing presets
- Improves tests: now we are using different logic inside `assert_errors`
- Improves tests: now testing magic numbers in more situations
- Improves tests: now testing more situations with empty base classes
- Improves tests: now testing presets, that they have all the existing visitors
- Improves tests: now using stricter `noqa` checks
- Improves tests: now testing that any name is allowed when using a variable
- Improves types: now all class attributes are marked as `ClassVar`
- Improves types: now we use `final` to indicate what should not be changed
- Improves types: now we do not have any ugly import hacks


## 0.2.0 aka Revenge of the Async

This release was made possible by awesome people who contributed
to the project during `#hactoberfest`. List of awesome people:

- [@novikovfred](https://github.com/novikovfred)
- [@AlwxSin](https://github.com/AlwxSin)
- [@TyVik](https://github.com/TyVik)
- [@AlexArcPy](https://github.com/AlexArcPy)
- [@tommbee](https://github.com/tommbee)

### Features

- Now we are counting `async` function as a module member
- We now forbid to use `credits()` builtin function
- We now check `async for` and `async with` nesting level
- We now check `async for` and `async with` variable names
- We now count `async` methods as method for classes complexity check
- We now count `async` functions as functions for module complexity check
- We now check `async` functions names and arguments
- We now count `async` functions complexity
- We now ignore `async` functions in jones complexity check
- We now check for nested `async` functions
- We now check for `async` functions with `@staticmethod` decorator

### Misc

- Improves docs: add `usage.rst`
- Improves docs: adds naming convention to the `naming.py`
- Improves docs: multiple typos, bugs, and issues fixes
- Improves tests: now we are testing `async` comprehensions


## Version 0.1.0

### Features

- **Breaking**: changes violation codes, now they are grouped by meaning

### Misc

- Refactoring: changes how visitors are organized inside the package
- Improves docs: now we have a glossary
- Refactoring: refactoring terms that violate our glossary
- Improves docs: now all error files contain fancy documentation and summary
- Improves docs: now we have added API reference to the docs
- Improves docs: adds new plugin development guide

## Version 0.0.16

### Features

- Adds `flake8-logging-format` dependency
- Adds `flake8-type-annotations` dependency
- Adds `flake8-breaking-line` dependency
- Removes `flake8-super-call` dependency
- Adds `PartialFloatViolation`
- Adds `MagicNumberViolation`
- Adds `WrongDocCommentViolation`
- Adds `MAGIC_NUMBERS_WHITELIST` constant
- Changes what variable names are blacklisted, adds `false`, `true`, and `no`

### Misc

- Improves docs: now including docs for `--max-condition` option
- Improves docs: adds some new `Zen of Python` references
- Improves tests: adds many new examples
- Improves docs: now each error has its error message displayed in the docs
- Improves docs: readme is now ready for the release
- Improves docs: now error pages are split
- Improves docs: now all `flake8` plugin dependencies are documented


## Version 0.0.15

### Features

- Adds `MultipleIfsInComprehensionViolation`
- Adds `TooManyConditionsViolation`
- Adds `--max-conditions` option

### Misc

- Improves `CONTRIBUTING.md`
- Moves issues templates to `.github/` folder
- Update error thrown on `RedundantSubscriptViolation`


## Version 0.0.14

### Features

- Adds `WrongModuleNamePatternViolation`
  and `WrongModuleNameUnderscoresViolation`
- Adds `TooManyImportsViolation` error and `--max-imports` option
- Adds `--i-control-code` option to ignore `InitModuleHasLogicViolation`
- Adds check for underscored numbers
- Forbids `u''` strings
- Adds `noqa` and `type` comments checks

### Misc

- Changes how many errors are generated for limits violations
- Refactors how visitors are injected into the checker, now using presets
- Creates new visitor type: `BaseTokenVisitor` for working with `tokenize`
- Improves typing support
- Adds `flake8-bandit` plugin
- Adds `flake8-eradicate` plugin
- Adds `flake8-print` plugin for development
- Removes `delegate` concept from the codebase


## Version 0.0.13 aka The Jones Complexity

### Features

- Adds `jones` complexity checker
- Adds `--max-line-complexity` and `--max-jones-score` options

### Misc

- Improves docs: adds detailed installation instructions
- Removes `flake8-blind-except` plugin


## Version 0.0.12

This is just a supporting release.
There are no new features introduced.

We have **changed** the error codes for general checks.

### Bugfixes

- Fixes bug with [nested imports missing `parent`](https://github.com/wemake-services/wemake-python-styleguide/issues/120)
- Fixes bug with [incorrect `pycodestyle` version](https://github.com/wemake-services/wemake-python-styleguide/issues/118)
- Removes `BareRaiseViolation` as it does not fit the purpose of this package

### Misc

- Improves docs: now all errors are sorted by `code`
- Improves docs: now all errors have reasoning
- Improves docs: some references are now clickable in web version
- Improves docs: now docs include `CHANGELOG.md`
- Improves docs: now we have templates for `bug` and `rule-request`
- Replaced `pytest-isort` with `flake8-isort`


## Version 0.0.11

This is just a supporting release.
There are no new features introduced.

### Bugfixes

- Fixes [`python3.7` support](https://github.com/wemake-services/wemake-python-styleguide/issues/93)
- Fixes [`AttributeError: 'ExceptHandler' object has no attribute 'depth'`](https://github.com/wemake-services/wemake-python-styleguide/issues/112)

### Misc

- Introduced the concept of regression testing, see `test/fixtures/regression`
- Removed `compat.py`
- Fixes some minor typos, problems, markup inside the docs
- Adds some new configuration to `sphinx`
- Changes `sphinx` docs structure a little bit

## Version 0.0.10 aka The Module Reaper

### Features

- Adds `WrongModuleNameViolation`, `WrongModuleMagicNameViolation`,
  and `TooShortModuleNameViolation`
- Adds `--min-module-name-length` config option
- Adds a blacklist of module names
- Adds `InitModuleHasLogicsViolation`
- Adds `EmptyModuleViolation`
- Adds a whitelist of magic module names

### Bugfixes

- Fixes `Option` class to have have incorrect `type` field, now using strings
- Fixes that `WrongStringTokenVisitor` was not activated

### Misc

- Improved typing support
- Now each error has a link to the corresponding constant (if any)
- Improved docs with links to the corresponding configuration flags


## Version 0.0.9

This is just a supporting release.
There are no new features introduced.

### Bugfixes

- Fixes `Attribute has no 'id'` error
- Fixes `missing 'typing_extension'` error

### Misc

- Errors are now tested
- Complexity tests are refactored


## Version 0.0.8 aka The Complex Complexity

### Features

- Now all dependencies are direct, they will be installed together
  with this package
- Adds direct dependencies, now there's no need to install any extra packages
- Adds `TooDeepNestingViolation` and `TooManyElifsViolation` checks
- Adds `--max-offset-blocks` and `--max-elifs` options
- Adds `TooManyModuleMembersViolation` and `TooManyMethodsViolation` checks
- Adds `--max-module-members` and `--max-methods` options
- Restricts to use `f` strings

### Bugfixes

- Removes incorrect `generic_visit()` calls
- Removes some unused `getattr()` calls
- Refactors how options are registered

### Misc

- Improved type support for options parsing


## Version 0.0.7

### Features

- Added new magic methods to the black list
- We now do not count `_` as a variable in `TooManyLocals` check
- We now restrict to nest `lambda`s
- We now allow to configure the minimal variable's name length via `setup.cfg`

### Misc

- Refactored how complexity checks are defined
- Refactored how errors are defined
- Now each check has strict `Raises:` policy which lists all possible errors
  that this check can find and raise
- Changed how visitors are initialized in tests
- Tests now cover nested classes' explicit bases
- Tests now cover nested classes and functions `noqa` comment


## Version 0.0.6

### Features

- We now check import aliases to be different from the original name
- Default complexity checks' values have changed

### Bugfixes

- ReadTheDocs build is fixed by providing extra dependencies
- Changed how local variables are counted

### Misc

- Improved typing support
- Added new documentation sections


## Version 0.0.5

### Features

- We now allow `generator_stop` to be a `__future__` import
- We now restrict dotted raw imports like: `import os.path`
- We now check import aliases as regular variable names

### Misc

- We have added a `CONTRIBUTING.md` file to help new contributors


## Version 0.0.4

### Features

- We now check `class`es to match our styleguide
- Classes have their own error group `Z3`
- Using `@staticmethod` is now forbidden
- Declaring `object` as a base class is now required
- Now we check that `__del__` magic method is not used
- Variable names `async` and `await` are forbidden
- We now forbid to use `__future__` imports
- We now have a whitelist for `__future__` imports
- Imports are now have its own subgroup `Z10`
- General rules now start from `Z11`


## Version 0.0.3

### Features

- We now use `Z` as the default code for our errors
- We have shuffled errors around, changing code and formats
- Now all name errors share the same class
- Adds `PrivateNameViolation`
- Now imports inside any structures rather than `Module` raises an error
- Adds `file` and `klass` as restricted names
- Now `__import__` is just a bad function name, not a special case
- Now version is defined in `poetry.toml` only
- We now have configuration! And it covers all design errors

### Bugfixes

- Fixes issue with missing `parent`s :batman:
- Fixes issue with `_$NAME` patterns being ignored


## Version 0.0.2

### Features

- Adds some new blacklisted variables' names
- Adds docs for each existing error code
- Adds whitelisted names for nested functions: `decorator` and `factory`
- Adds new blacklisted module's metadata variables
- Removed `BAD_IMPORT_FUNCTIONS` variable, now just checking `__import__`

### Testing

- Add gen-tests that cover most of the issues
- Removed almost all integration tests, saving just a few of them

### Misc

- Adds `poetry` as the main project tool
- Adds `shpinx` as a documentation tool


## Version 0.0.1

- Initial release
