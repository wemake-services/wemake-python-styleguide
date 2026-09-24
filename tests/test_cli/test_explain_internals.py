"""Unit testing of wps explain command."""

from typing import Final

import pytest

from wemake_python_styleguide.cli.commands.explain import (
    violation_loader,
)
from wemake_python_styleguide.cli.commands.explain.message_formatter import (
    format_violation,
)
from wemake_python_styleguide.violations.best_practices import (
    InitModuleHasLogicViolation,
)
from wemake_python_styleguide.violations.naming import (
    UpperCaseAttributeViolation,
)
from wemake_python_styleguide.violations.oop import BuiltinSubclassViolation

_NOT_FOUND_CODE_VIOLATION: Final = 999


def _make_violation(docstring: str) -> violation_loader.ViolationInfo:
    """Create a stub violation with the given docstring."""
    return violation_loader.ViolationInfo(
        identifier='StubViolation',
        code=_NOT_FOUND_CODE_VIOLATION,
        docstring=docstring,
        section='best_practices',
    )


@pytest.mark.parametrize(
    ('broken_path', 'bad_prefix'),
    [
        (
            'Default: :str:`wemake_python_styleguide.options.NON_EXISTENT`',
            ':str:',
        ),
        ('Default: :str:`a.b.c`', ':str:'),
        (
            ':py:data:`~wemake_python_styleguide.constants.NON_EXISTENT`',
            ':py:data:`~',
        ),
        (
            ':py:data:`~.some_folder.constants.MAX_VALUE`',
            ':py:data:`~.',
        ),
    ],
)
def test_format_violation_unresolved_reference(broken_path, bad_prefix):
    """Fallback keeps a plain-text path for unresolvable references."""
    result_docstring_violation = format_violation(_make_violation(broken_path))

    assert bad_prefix not in result_docstring_violation


@pytest.mark.parametrize(
    'violation_params',
    [
        (115, UpperCaseAttributeViolation),
        (412, InitModuleHasLogicViolation),
        (600, BuiltinSubclassViolation),
    ],
)
def test_violation_getter(violation_params):
    """Test that violation loader can get violation by their codes."""
    violation_code, expected_class = violation_params
    violation = violation_loader.get_violation(violation_code)
    assert violation.code is not None
    assert violation.docstring == expected_class.__doc__
