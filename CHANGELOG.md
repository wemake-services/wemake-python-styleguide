# Version history

We follow Semantic Versions since the `0.1.0` release.
We used to have incremental versioning before `0.1.0`.


## WIP

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

### Bugfixes

- Fixes a lot of rules that were ignoring `Bytes` node as constant type
- Fixes location of the `BooleanPositionalArgumentViolation`
- Fixes argument count issue with `async` functions
- Fixes `WrongConditionalVisitor` not detecting `tuple` as constants
- Fixes `WrongConditionalVisitor` not detecting negative numbers as constants
- Fixes some magic number that were not detected based on their location
- Fixes error when regular functions named as blacklisted
  magic methods were forbidden, now we check for methods only

### Misc

- Adds `safety` and other dependency checks to the CI process
- Improves tests: now `tokenize` works differently inside tests
- Improves tests: now testing more brackets cases aka "magic coverage bug"
- Improves docs: adds new badge about our code style
- Refactoring: trying to use `astor` where possible to simplify the codebase
- Refactoring: introduces some new `transformations`
- Improves tests: changes how `flake8` is executed, now it is twice as fast
- Improves docs: now linting `conf.py` with `flake8`


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


## Bugfixes

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
- Fixes that `WrongStringVisitor` was not activated

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
