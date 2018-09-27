# Version history

We follow Semantic Versions since the `0.1.0` release.
We used to have incremental versioning before `0.1.0`.

## Version 0.0.16

### Features

- Adds `PartialFloatViolation`
- Adds `MagicNumberViolation`
- Adds `MAGIC_NUMBERS_WHITELIST` constant
- Changes what variable names are blacklisted, adds `false`, `true`, and `no`

### Misc

- Improves docs: now including docs for `--max-condition` option
- Improves docs: adds some new `zen` references
- Improves tests: adds many new examples
- Improves docs: now each error has its error message displayed in the docs


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
