from dataclasses import dataclass

import pytest

from wemake_python_styleguide.cli.commands.explain import violation_loader, message_formatter
from wemake_python_styleguide.cli.commands.explain.violation_loader import ViolationInfo
from wemake_python_styleguide.violations.best_practices import InitModuleHasLogicViolation
from wemake_python_styleguide.violations.naming import UpperCaseAttributeViolation
from wemake_python_styleguide.violations.oop import BuiltinSubclassViolation


@pytest.mark.parametrize(
    'violation_params',
    [
        (115, UpperCaseAttributeViolation),
        (412, InitModuleHasLogicViolation),
        (600, BuiltinSubclassViolation),
    ]
)
def test_violation_getter(violation_params):
    violation_code, expected_class = violation_params
    violation = violation_loader.get_violation(violation_code)
    assert violation.code is not None
    assert violation.docstring == expected_class.__doc__


@pytest.mark.parametrize(
    'test_params',
    [
        (
            '  text\n  text\n  text',
            'text\ntext\ntext'
        ),
        (
            '  text\n\ttext\r\n  text',
            'text\n  text\ntext'
        ),
    ]
)
def test_indentation_removal(test_params):
    input_text, expected = test_params
    actual = message_formatter._remove_indentation(input_text)
    assert actual == expected


violation = ViolationInfo(
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
    formatted = message_formatter.format_violation(violation)
    assert formatted == violation_string
