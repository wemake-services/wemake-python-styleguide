"""Test that wps explain command works fine."""

import os
import platform
import subprocess

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
        (' text\n    \n\n text', 'text\n   \n\ntext'),
        ('\n\n', '\n\n'),
        ('text', 'text'),
        ('text\ntext', 'text\ntext'),
        ('', ''),
        ('    ', '    '),
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
violation_string = 'docstring\n\nSee at website: https://pyflak.es/WPS100'


def test_formatter():
    """Test that formatter formats violations as expected."""
    formatted = message_formatter.format_violation(violation_mock)
    assert formatted == violation_string


def _popen_in_shell(args: str) -> subprocess.Popen:  # pragma: no cover
    """Run command in shell."""
    encoding = 'utf-8'
    # Some encoding magic. Calling with shell=True on Windows
    # causes everything to be in cp1251. shell=True is needed
    # for subprocess.Popen to locate the installed wps command.
    if platform.system() == 'Windows':
        encoding = 'cp1251'
    return subprocess.Popen(  # noqa: S602 (insecure shell=True)
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding=encoding,
        env=os.environ,
        shell=True,
    )


def test_command(snapshot):
    """Test that command works and formats violations as expected."""
    process = _popen_in_shell('wps explain WPS123')
    stdout, stderr = process.communicate()
    assert process.returncode == 0, (stdout, stderr)
    assert stdout == snapshot


@pytest.mark.parametrize(
    'command',
    [
        'wps explain 10000',
        'wps explain NOT_A_CODE',
        'wps explain WPS10000',
    ],
)
def test_command_on_not_found(command, snapshot):
    """Test command works when violation code is wrong."""
    process = _popen_in_shell(command)
    stdout, stderr = process.communicate()
    assert process.returncode == 1, (stdout, stderr)
    assert stderr == snapshot


def test_no_command_specified(snapshot):
    """Test command displays error message when no subcommand provided."""
    process = _popen_in_shell('wps')
    stdout, stderr = process.communicate()
    assert process.returncode == 1, (stdout, stderr)
    assert stderr == snapshot
