"""Provides tools to extract violation info."""

import importlib
import inspect
from collections.abc import Collection, Mapping
from types import ModuleType
from typing import Final, final

from attrs import frozen

from wemake_python_styleguide.violations.base import BaseViolation

_VIOLATION_SUBMODULES: Final = (
    'best_practices',
    'complexity',
    'consistency',
    'naming',
    'oop',
    'refactoring',
    'system',
)
_VIOLATION_MODULE_BASE: Final = 'wemake_python_styleguide.violations'


@final
@frozen
class ViolationInfo:
    """Contains violation info."""
    identifier: str
    fully_qualified_id: str
    code: int
    docstring: str
    section: str


def _is_a_violation(class_object) -> bool:
    """Check if class is a violation class."""
    return (
        issubclass(class_object, BaseViolation) and
        hasattr(class_object, 'code')  # Not all subclasses have code
    )


def _get_violations_of_submodule(
    module: ModuleType,
) -> Collection[type[BaseViolation]]:
    """Get all violation classes of defined module."""
    return [
        class_
        for name, class_ in inspect.getmembers(module, inspect.isclass)
        if _is_a_violation(class_)
    ]


def _create_violation_info(
    class_object, submodule_name: str, submodule_path: str
) -> ViolationInfo:
    """Create violation info DTO from violation class and metadata."""
    return ViolationInfo(
        identifier=class_object.__name__,
        fully_qualified_id=f'{submodule_path}.{class_object.__name__}',
        code=class_object.code,
        docstring=class_object.__doc__,
        section=submodule_name,
    )


def _get_all_violations() -> Mapping[int, ViolationInfo]:
    """Get all violations inside all defined WPS violation modules."""
    all_violations = {}
    for submodule_name in _VIOLATION_SUBMODULES:
        submodule_path = f'{_VIOLATION_MODULE_BASE}.{submodule_name}'
        violations = _get_violations_of_submodule(
            importlib.import_module(submodule_path)
        )
        for violation in violations:
            all_violations[violation.code] = _create_violation_info(
                violation,
                submodule_name,
                submodule_path,
            )
    return all_violations


def get_violation(code: int) -> ViolationInfo | None:
    """Get a violation by its integer code."""
    violations = _get_all_violations()
    if code not in violations:
        return None
    return violations[code]
