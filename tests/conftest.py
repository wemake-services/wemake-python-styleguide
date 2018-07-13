# -*- coding: utf-8 -*-

import inspect
import os
from operator import itemgetter

import pytest

from wemake_python_styleguide import errors


def _is_error_class(cls) -> bool:
    return (
        inspect.isclass(cls) and
        issubclass(cls, errors.BaseStyleViolation) and
        cls is not errors.BaseStyleViolation
    )


@pytest.fixture(scope='module')
def all_errors():
    """Loads all errors from the package."""
    return list(
        map(itemgetter(1), inspect.getmembers(errors, _is_error_class)),
    )


@pytest.fixture(scope='session')
def absolute_path():
    """Fixture to create full path relative to `contest.py` inside tests."""
    def factory(*files):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, *files)

    return factory
