# How to contribute

## Tutorials

If you want to start working on this project,
you will need to get familiar with these APIs:

- Writing a `flake8` [plugin](http://flake8.pycqa.org/en/latest/plugin-development/)
- Using `ast` [module](https://docs.python.org/3/library/ast.html)
- [Tokenizer for Python source](https://docs.python.org/3/library/tokenize.html)
- [Tokens tutorial](https://www.asmeurer.com/brown-water-python/tokens.html)

It is also recommended to take a look at these resources:

- Visual tool to explore [python's ast](https://python-ast-explorer.com/) (very useful, but outdated!)
- Missing `ast` [guide](https://greentreesnakes.readthedocs.io/en/latest/)
- List of `python` [static analysis tools](https://github.com/vintasoftware/python-linters-and-code-analysis)
- List of `flake8` [extensions](https://github.com/DmytroLitvinov/awesome-flake8-extensions)


## First steps

1. Fork [our repo](https://github.com/wemake-services/wemake-python-styleguide), here's the [guide on forking](https://help.github.com/en/github/getting-started-with-github/fork-a-repo)
2. [Clone your new repo](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) (forked repo) to have a local copy of the code
3. Apply the required changes! See developer docs on how to work with the code
4. Send a Pull Request to our original repo. Here's [the helpful guide](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request) on how to do that


## Developer's documentation

Make sure that you are familiar with [developer's documentation](https://wemake-python-styleguide.rtfd.io/en/latest/pages/api/index.html).

That's a main starting point to the future development.
You can jump start into the development of new rules by reading ["Creating a new rule tutorial"](https://wemake-python-styleguide.rtfd.io/en/latest/pages/api/tutorial.html).


## Dependencies

We use [poetry](https://github.com/sdispater/poetry) to manage the dependencies.

To install them you would need to run `install` command:

```bash
poetry install
```

To activate your `virtualenv` run `poetry shell`.

### Adding new flake8 plugins

If you are adding a `flake8` plugin dependency (not dev-dependency),
you will have to do several things:

1. Install plugin with `poetry`
2. Add docs about the error code to the `pages/usage/violations/index.rst`
3. Add a test that the plugin is working to `tests/test_plugins.py`

## One magic command

Run `make test` to run everything we have!

### Building on Windows

- Building directly in Windows does not work.
- Instead, use a Windows Subsystem for Linux (WSL) such as Ubuntu 18.04 LTS that you can get from the Microsoft Store.
- Clone the project to a part of the WSL where Windows does not overwrite permissions, for example _directly to the home of the WSL_ (do `cd` and then `git clone`). That problem looks like [this](https://github.com/wemake-services/wemake-python-styleguide/issues/1007#issuecomment-562719702) and you can read more about why changing the permissions does not work [here](https://github.com/Microsoft/WSL/issues/81).


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
flake8 .
```

These steps are mandatory during the CI.


## Architecture

We use [import-linter](https://import-linter.readthedocs.io)
to enforce strict layered architecture.

```bash
lint-imports
```

See `.importlinter` file for contracts definition.
All contracts must be valid for each commit.
This step is mandatory during the CI.


## Type checks

We use `mypy` to run type checks on our code.
To use it:

```bash
mypy wemake_python_styleguide
```

This step is mandatory during the CI.


## Spellcheckers

This project is developed by a diverse and multilingual group of people.
Many of us are not English native speakers and we also know that people can make mistakes and typos even in the simplest of words.

So, that's why we use a bunch of tools to find and fix spelling and grammar.

You will need to install them manually, because we don't ship them with the dependencies:

```bash
pip install codespell flake8-spellcheck
```

And then you can use them:

```bash
# codespell:
codespell -w wemake_python_styleguide tests docs scripts styles *.md

# flake8-spellcheck:
flake8 --whitelist ./tests/whitelist.txt .
```

We run them from time to time, this is not in the CI yet.


## Helpers

We also have several helpers to make your development work easier:

- `astboom` is used to visualize `ast` nodes in other python modules,
  usage: `astboom ast < my_module.py`
- `tokelor` is used to visualize tokens in other python modules,
  usage: `tokelor my_module.py`


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
10. Run `lint-imports` to ensure that architecture contracts are correct
11. Run `doc8` to ensure that docs are correct

You can run everything at once with `make test`,
see our `Makefile` for more details.


## Notes for maintainers

This section is intended for maintainers only.
If you are not a maintainer (or do not know what it means),
just skip it. You are not going to miss anything useful.

### Releasing a new version

Releasing a new version requires several steps:

1. Ensure that `CHANGELOG.md` is up-to-date and contains all changes
2. Bump version in `pyproject.toml`
3. Bump version in `Dockerfile` that is used for Github Action
4. Run `git commit -a -m 'Version x.y.z release' && git tag -a x.y.x -m 'Version x.y.z' && git push && git push --tags`
5. Run `poetry publish --build`
6. Edit Github Release and mark that new action version is released

Done! New version is released.

### Making patches to older versions

If you want to release a patch for an older version, that what you have to do:

1. Check out the previous `tag`
2. Create a new branch relative to this tag:
   `git checkout $TAG_NAME; git checkout -b $RELEASE_NAME`
3. Merge it into master, there might be some `rebase` and `cherry-pick`
   involved during this operation


## Other help

You can contribute by spreading a word about this library.
It would also be a huge contribution to write
a short article on how you are using this project.
You can also share your best practices with us.

You can also consider donations to the project:
- <https://opencollective.com/wemake-python-styleguide>
- <https://issuehunt.io/r/wemake-services/wemake-python-styleguide>

Number of current supporters:

[![Supporters](https://img.shields.io/opencollective/all/wemake-python-styleguide.svg?color=gold&label=supporters)](https://opencollective.com/wemake-python-styleguide)


## List of contributors

Here are the awesome people who contributed to our project:

[![List of contributors](https://opencollective.com/wemake-python-styleguide/contributors.svg?width=890&button=0)](https://github.com/wemake-services/wemake-python-styleguide/graphs/contributors)
