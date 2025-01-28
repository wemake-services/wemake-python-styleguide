"""Provides tools to extract violation info."""

import inspect
from collections.abc import Collection, Mapping
from types import ModuleType
from typing import final

from attrs import frozen

from wemake_python_styleguide.cli.commands.explain.module_loader import (
    get_violation_submodules,
)
from wemake_python_styleguide.violations.base import BaseViolation


@final
@frozen
class ViolationInfo:
    """Contains violation info."""

    identifier: str
    code: int
    docstring: str
    section: str


def _is_a_violation(class_object) -> bool:
    """Check if class is a violation class."""
    try:
        return (
            issubclass(class_object, BaseViolation)
            and hasattr(class_object, 'code')  # Only end-user classes have code
        )
    except TypeError:  # pragma: no cover
        # py 3.10 bug raises a type error
        return False


def _get_violations_of_submodule(
    module: ModuleType,
) -> Collection[type[BaseViolation]]:
    """Get all violation classes of defined module."""
    return [
        class_
        for name, class_ in inspect.getmembers(module, inspect.isclass)
        if _is_a_violation(class_)
    ]


def _create_violation_info(class_object, submodule_name: str) -> ViolationInfo:
    """Create violation info DTO from violation class and metadata."""
    return ViolationInfo(
        identifier=class_object.__name__,
        code=class_object.code,
        docstring=class_object.__doc__,
        section=submodule_name,
    )


def _get_all_violations() -> Mapping[int, ViolationInfo]:
    """Get all violations inside all defined WPS violation modules."""
    all_violations = {}
    for submodule in get_violation_submodules():
        violations = _get_violations_of_submodule(submodule)
        for violation in violations:
            all_violations[violation.code] = _create_violation_info(
                violation,
                submodule.__name__,
            )
    return all_violations


def get_violation(code: int) -> ViolationInfo | None:
    """Get a violation by its integer code."""
    violations = _get_all_violations()
    if code not in violations:
        return None
    return violations[code]
