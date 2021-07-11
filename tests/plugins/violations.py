import inspect
from operator import attrgetter, itemgetter

import pytest

from wemake_python_styleguide.violations import (
    best_practices,
    complexity,
    consistency,
    naming,
    oop,
    refactoring,
    system,
)
from wemake_python_styleguide.violations.base import (
    ASTViolation,
    BaseViolation,
    MaybeASTViolation,
    SimpleViolation,
    TokenizeViolation,
)

VIOLATIONS_MODULES = (
    system,
    naming,
    complexity,
    consistency,
    best_practices,
    refactoring,
    oop,
)

_SESSION_SCOPE = 'session'


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
    classes = {}
    for module in VIOLATIONS_MODULES:
        classes_names_list = inspect.getmembers(module, _is_violation_class)
        only_classes = map(itemgetter(1), classes_names_list)
        classes.update({
            module: sorted(only_classes, key=attrgetter('code')),
        })
    return classes


@pytest.fixture(scope=_SESSION_SCOPE)
def all_violations():
    """Loads all violations from the package and creates a flat list."""
    classes = _load_all_violation_classes()
    all_errors_container = []
    for module_classes in classes.values():
        all_errors_container.extend(module_classes)
    return all_errors_container


@pytest.fixture(scope=_SESSION_SCOPE)
def all_controlled_violations():
    """Loads all violations which may be tweaked using `i_control_code`."""
    classes = _load_all_violation_classes()
    controlled_errors_container = []
    for module_classes in classes.values():
        for violation_class in module_classes:
            if '--i-control-code' in violation_class.__doc__:
                controlled_errors_container.append(violation_class)
    return controlled_errors_container


@pytest.fixture(scope=_SESSION_SCOPE)
def all_module_violations():
    """Loads all violations from the package."""
    return _load_all_violation_classes()


@pytest.fixture(scope=_SESSION_SCOPE)
def all_violation_codes(all_module_violations):
    """Loads all codes and their violation classes from the package."""
    return {
        module: {
            violation.code: violation
            for violation in all_module_violations[module]
        }
        for module in all_module_violations.keys()
    }
