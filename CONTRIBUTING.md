# How to contribute

## Tutorials

If you want to start working on this project,
you will need to get familiar with these APIs:

- Writing a `flake8` [plugin](http://flake8.pycqa.org/en/latest/plugin-development/)
- Using `ast` [module](https://docs.python.org/3/library/ast.html)
- [Tokenizer for Python source](https://docs.python.org/3/library/tokenize.html)

It is also recommended to take a look at these resources:

- Visual tool to explore [`python's ast`](https://python-ast-explorer.com/) (very useful!)
- Missing `ast` [guide](https://greentreesnakes.readthedocs.io/en/latest/)
- List of `python` [static analysis tools](https://github.com/vintasoftware/python-linters-and-code-analysis)
- List of `flake8` [extensions](https://github.com/DmytroLitvinov/awesome-flake8-extensions)


## Developer's documentation

Make sure that you are familiar with [developer's documentation](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/api.html).

That's a main starting point to the future development.
You can jump start into the development of new rules by reading ["Creating a new rule tutorial"](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/tutorial.html).


## Dependencies

We use [`poetry`](https://github.com/sdispater/poetry) to manage the dependencies.

To install them you would need to run `install` command:

```bash
poetry install
```

To activate your `virtualenv` run `poetry shell`.

### Adding new flake8 plugins

If you are adding a `flake8` plugin dependency (not dev-dependency),
you will have to do several things:

1. Install plugin with `poetry`
2. Add docs about the error code to the `errors/index.rst`
3. Add a test that the plugin is working to `tests/test_plugins.py`


## Tests

We use `pytest` and `flake8` for quality control.
We also use `wemake_python_styleguide` itself
to develop `wemake_python_styleguide`.

To run all tests:

```bash
pytest
```

To run linting:

```bash
flake8 wemake_python_styleguide tests docs
```

These steps are mandatory during the CI.


## Architecture

We use [`layer-lint`](https://layer-linter.readthedocs.io/en/latest/usage.html)
to enforce strict layered architecture.

```bash
layer-lint wemake_python_styleguide
```

All contracts must be valid for each commit.
This step is mandatory during the CI.


## Type checks

We use `mypy` to run type checks on our code.
To use it:

```bash
mypy wemake_python_styleguide
```

This step is mandatory during the CI.


## Submitting your code

We use [trunk based](https://trunkbaseddevelopment.com/)
development (we also sometimes call it `wemake-git-flow`).

What the point of this method?

1. We use protected `master` branch,
   so the only way to push your code is via pull request
2. We use issue branches: to implement a new feature or to fix a bug
   create a new branch named `issue-$TASKNUMBER`
3. Then create a pull request to `master` branch
4. We use `git tag`s to make releases, so we can track what has changed
   since the latest release

So, this way we achieve an easy and scalable development process
which frees us from merging hell and long-living branches.

In this method, the latest version of the app is always in the `master` branch.

### Making patches to older versions

If you want to release a patch for an older version, that what you have to do:

1. Check out the previous `git tag`
2. Create a new branch relative to this tag
3. Merge it into master, there might be some `rebase` and `cherry-pick`
   involved during this operation

### Before submitting

Before submitting your code please do the following steps:

1. Run `pytest` to make sure everything was working before
2. Add any changes you want
3. Add tests for the new changes
4. Add an integration test into `tests/fixtures/noqa.py`
5. Edit documentation if you have changed something significant
6. Update `CHANGELOG.md` with a quick summary of your changes
7. Run `pytest` again to make sure it is still working
8. Run `mypy` to ensure that types are correct
9. Run `flake8` to ensure that style is correct
10. Run `layer-lint` to ensure that architecture contracts are correct
11. Run `doc8` to ensure that docs are correct


## Other help

You can contribute by spreading a word about this library.
It would also be a huge contribution to write
a short article on how you are using this project.
You can also share your best practices with us.
