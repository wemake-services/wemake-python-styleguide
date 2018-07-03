# wemake-python-styleguide

[![wemake.services](https://img.shields.io/badge/style-wemake.services-green.svg?label=&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](http://wemake.services)
[![Build Status](https://travis-ci.org/wemake-services/wemake-python-styleguide.svg?branch=master)](https://travis-ci.org/wemake-services/wemake-python-styleguide)
[![Coverage](https://coveralls.io/repos/github/wemake-services/wemake-python-styleguide/badge.svg?branch=master)](https://coveralls.io/github/wemake-services/wemake-python-styleguide?branch=master)
[![PyPI version](https://badge.fury.io/py/wemake-python-styleguide.svg)](https://badge.fury.io/py/wemake-python-styleguide)
[![Documentation Status](https://readthedocs.org/projects/wemake-python-styleguide/badge/?version=latest)](https://wemake-python-styleguide.readthedocs.io/en/latest/?badge=latest)


Welcome to the most opinionated linter ever.


## Installation

```bash
pip install wemake-python-styleguide
```

## Project status

We are in early alpha.
Use it on your own risk.


## Running tests

Clone the repository, install `poetry`, then do from within the project folder:

```bash
# Installing dependencies (only required to be run once):
poetry install
poetry develop

# Running tests:
poetry run pytest
poetry run mypy wemake_python_styleguide
poetry run doc8 -q docs
```

It's OK if some tests are skipped.
