"""Test that wps explain command works fine."""

import pytest

from wemake_python_styleguide.cli.commands.explain import (
    message_formatter,
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


@pytest.mark.parametrize(
    'test_params',
    [
        ('  text\n  text\n  text', 'text\ntext\ntext'),
        ('  text\n\ttext\r\n  text', 'text\n  text\ntext'),
    ],
)
def test_indentation_removal(test_params):
    """Test that indentation remover works in different conditions."""
    input_text, expected = test_params
    actual = message_formatter._remove_indentation(input_text)  # noqa: SLF001
    assert actual == expected


violation_mock = violation_loader.ViolationInfo(
    identifier='Mock',
    code=100,
    docstring='docstring',
    fully_qualified_id='mock.Mock',
    section='mock',
)
violation_string = (
    'WPS100 (Mock)\n'
    'docstring\n'
    'See at website: https://wemake-python-styleguide.readthedocs.io/en/'
    'latest/pages/usage/violations/mock.html#mock.Mock'
)


def test_formatter():
    """Test that formatter formats violations as expected."""
    formatted = message_formatter.format_violation(violation_mock)
    assert formatted == violation_string
