# Version history

We follow Semantic Versions.

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
