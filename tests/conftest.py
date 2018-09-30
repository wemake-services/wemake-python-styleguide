# -*- coding: utf-8 -*-

import inspect
import os
from operator import itemgetter

import pytest

from wemake_python_styleguide import errors
from wemake_python_styleguide.errors.base import (
    ASTStyleViolation,
    BaseStyleViolation,
    SimpleStyleViolation,
    TokenStyleViolation,
)


def _is_error_class(cls) -> bool:
    base_classes = {
        ASTStyleViolation,
        BaseStyleViolation,
        SimpleStyleViolation,
        TokenStyleViolation,
    }

    return (
        inspect.isclass(cls) and
        issubclass(cls, BaseStyleViolation) and
        cls not in base_classes
    )


def _load_all_error_classes():
    modules = [
        errors.naming,
        errors.complexity,
        errors.consistency,
        errors.best_practices,
    ]

    classes = {}
    for module in modules:
        classes_names_list = inspect.getmembers(module, _is_error_class)
        only_classes = map(itemgetter(1), classes_names_list)
        classes.update({module: list(only_classes)})
    return classes


@pytest.fixture(scope='session')
def all_errors():
    """Loads all errors from the package."""
    classes = _load_all_error_classes()
    all_errors_container = []
    for module_classes in classes.values():
        all_errors_container.extend(module_classes)
    return all_errors_container


@pytest.fixture(scope='session')
def all_module_errors():
    """Loads all errors from the package."""
    return _load_all_error_classes()


@pytest.fixture(scope='session')
def absolute_path():
    """Fixture to create full path relative to `contest.py` inside tests."""
    def factory(*files):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, *files)

    return factory
