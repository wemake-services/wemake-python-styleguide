"""Unit testing of wps explain command."""

import pytest

from wemake_python_styleguide.cli.commands.explain import (
    violation_loader,
)
from wemake_python_styleguide.violations.best_practices import (
    InitModuleHasLogicViolation,
)
from wemake_python_styleguide.violations.naming import (
    UpperCaseAttributeViolation,
)
from wemake_python_styleguide.violations.oop import BuiltinSubclassViolation


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
