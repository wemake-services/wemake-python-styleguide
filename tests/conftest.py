# -*- coding: utf-8 -*-

import inspect
import os
from operator import itemgetter

import pytest

from wemake_python_styleguide import errors
from wemake_python_styleguide.errors.base import BaseStyleViolation


def _is_error_class(cls) -> bool:
    return (
        inspect.isclass(cls) and
        issubclass(cls, BaseStyleViolation) and
        cls is not BaseStyleViolation
    )


@pytest.fixture(scope='session')
def all_errors():
    """Loads all errors from the package."""
    modules = [
        errors.imports,
        errors.general,
        errors.classes,
        errors.complexity,
    ]

    classes = []
    for module in modules:
        classes.extend(inspect.getmembers(module, _is_error_class))

    return list(map(itemgetter(1), classes))


@pytest.fixture(scope='session')
def absolute_path():
    """Fixture to create full path relative to `contest.py` inside tests."""
    def factory(*files):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, *files)

    return factory
