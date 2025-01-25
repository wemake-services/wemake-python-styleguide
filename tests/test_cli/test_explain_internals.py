"""Unit testing of wps explain command."""

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
        (' text\n    \n\n text', 'text\n\n\ntext'),
        ('\n\n', '\n\n'),
        ('text', 'text'),
        ('text\ntext', 'text\ntext'),
        ('', ''),
        ('    ', ''),
    ],
)
def test_indentation_removal(test_params):
    """Test that indentation remover works in different conditions."""
    input_text, expected = test_params
    actual = message_formatter._remove_indentation(input_text)  # noqa: SLF001
    assert actual == expected


def test_formatter():
    """Test that formatter formats violations as expected."""
    violation_mock = violation_loader.ViolationInfo(
        identifier='Mock',
        code=100,
        docstring='docstring',
        section='mock',
    )
    violation_string = 'docstring\n\nSee at website: https://pyflak.es/WPS100'
    formatted = message_formatter.format_violation(violation_mock)
    assert formatted == violation_string
