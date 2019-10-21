# -*- coding: utf-8 -*-

import inspect
import os
from collections import namedtuple
from operator import attrgetter, itemgetter

import pytest

from wemake_python_styleguide.options.config import Configuration
from wemake_python_styleguide.violations import (
    annotations,
    best_practices,
    complexity,
    consistency,
    naming,
    oop,
    refactoring,
)
from wemake_python_styleguide.violations.base import (
    ASTViolation,
    BaseViolation,
    MaybeASTViolation,
    SimpleViolation,
    TokenizeViolation,
)


def _is_violation_class(cls) -> bool:
    base_classes = {
        ASTViolation,
        BaseViolation,
        SimpleViolation,
        TokenizeViolation,
        MaybeASTViolation,
    }
    if not inspect.isclass(cls):
        return False

    return issubclass(cls, BaseViolation) and cls not in base_classes


def _load_all_violation_classes():
    modules = [
        naming,
        complexity,
        consistency,
        best_practices,
        refactoring,
        oop,
        annotations,
    ]

    classes = {}
    for module in modules:
        classes_names_list = inspect.getmembers(module, _is_violation_class)
        only_classes = map(itemgetter(1), classes_names_list)
        classes.update({
            module: list(
                sorted(only_classes, key=attrgetter('code')),
            ),
        })
    return classes


@pytest.fixture(scope='session')
def all_violations():
    """Loads all violations from the package and creates a flat list."""
    classes = _load_all_violation_classes()
    all_errors_container = []
    for module_classes in classes.values():
        all_errors_container.extend(module_classes)
    return all_errors_container


@pytest.fixture(scope='session')
def all_module_violations():
    """Loads all violations from the package."""
    return _load_all_violation_classes()


@pytest.fixture(scope='session')
def absolute_path():
    """Fixture to create full path relative to `contest.py` inside tests."""
    def factory(*files):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, *files)

    return factory


@pytest.fixture(scope='session')
def options():
    """Returns the options builder."""
    default_values = {
        option.long_option_name[2:].replace('-', '_'): option.default
        for option in Configuration._options  # noqa: WPS437
    }

    Options = namedtuple('options', default_values.keys())

    def factory(**kwargs):
        final_options = default_values.copy()
        final_options.update(kwargs)
        return Options(**final_options)

    return factory


@pytest.fixture(scope='session')
def default_options(options):  # noqa: WPS442
    """Returns the default options."""
    return options()
