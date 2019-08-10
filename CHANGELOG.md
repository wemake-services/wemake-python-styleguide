# Version history

We follow Semantic Versions since the `0.1.0` release.
We used to have incremental versioning before `0.1.0`.


## 0.12.0 WIP

In this release we had a little focus on:

0. Primitives and constants and how to use them
1. Strings and numbers and how to write them
2. OOP features
3. Blocks and code structure,
   including variable scoping and overlaping variables
4. Overused expressions and new complexity metrics

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
- Forbids to have too long `try` bodies
- Forbids to overlap local and block variables
- Forbids to use block variables after the block definitions
- Changes how `WrongSlotsViolation` works, now `(...) + value` is restricted
  in favor of `(..., *value)`
- Forbids to have explicit unhashable types in sets and dicts
- Forbids to define useless overwritten methods
- Enforces `j` prefix over `J` for `complex` numbers
- Forbids overused expressions
- Forbids explicit `0` division, multiply, pow, addition, and substraction
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
- Forbids to use ``assert False`` and other false-constants
- Forbids to use ``while False:``  and other false-constants
- Forbids to use ``open()`` outside of ``with``
- Forbids to use ``type()`` for compares
- Forbids to have consecutive expressions with too deep access level
- Forbids to have too many public instance attributes

### Bugfixes

- Bumps `flake8-eradicate` version
  and solves `attrs` incompatible versions issue
- Bumps `flake8-dosctrings` veresion
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

### Misc

- Adds `bellybutton` to the list of linters
- Improves tests for binary, octal, hex, and expanetional numbers
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

We also have this [nice migration guide](https://wemake-python-stylegui.de/en/latest/pages/changelog/migration_to_0_11.html)
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
big cudos to the developers of this wonderful tool.

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
- Forbids to use heterogenous compares like `x == x > 0`
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
- Changes how `max-arguments` are counted.
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
- Improves docs: we have added a special graph to show our architecure
- Improves docs: we now have a clean page for `checker` without extra junk
- Improves docs: we now have a tutorial for creating new rules
- Refactoring: moves `presets` package to the root
- Improves tests: we now lint our layered architecure with `layer-lint`


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
- **Breaking**: changes `TooManyBaseClassesViolation` code from ``225`` to ``215``
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
- [@SheldonNunes ](https://github.com/SheldonNunes)
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
- Fixes [`AttributeError: 'ExceptHandler' object has no attribute 'depth' `](https://github.com/wemake-services/wemake-python-styleguide/issues/112)

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
