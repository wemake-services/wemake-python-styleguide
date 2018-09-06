# Version history

We follow Semantic Versions since the `0.1.0` release.


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
- Changed how visiters are initialized in tests
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
