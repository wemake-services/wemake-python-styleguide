# How to contribute

If you want to start working on this project,
you will need to get familiar with these APIs:

- [Writing a `flake8` plugin](http://flake8.pycqa.org/en/latest/plugin-development/)
- [Using `ast` module](https://docs.python.org/3/library/ast.html)
- [Tokenizer for Python source](https://docs.python.org/3/library/tokenize.html)

It is also recommended to take a look at these resources:

- [Missing `ast` guide](https://greentreesnakes.readthedocs.io/en/latest/)


## Dependencies

We use [`poetry`](https://github.com/sdispater/poetry) to manage the dependencies.

To install them you would need to run two commands:

```bash
poetry install
poetry develop
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

This step is mandatory during the CI.


## Type checks

We use `mypy` to run type checks on our code.
To use it:

```bash
mypy wemake_python_styleguide
```

This step is mandatory during the CI.


## Before submitting

Before submitting your code please do the following steps:

1. Run `pytest` to make sure everything was working before
2. Add any changes you want
3. Adds tests for the new changes
4. Edit documentation if you have changed something significant
5. Run `pytest` again to make sure it is still working
6. Run `mypy` to ensure that types are correct
7. Run `doc8` to ensure that docs are correct


## Other help

You can contribute by spreading a word about this library.
It would also be a huge contribution to write
a short article on how you are using this project.
What are your best-practices?
