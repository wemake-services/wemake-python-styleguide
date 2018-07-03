# Version history

We follow Semantic Versions.


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
