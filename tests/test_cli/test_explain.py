"""Test that wps explain command works fine."""

from io import BytesIO
from typing import TextIO

import pytest

from wemake_python_styleguide.cli.commands.explain import (
    message_formatter,
    violation_loader,
)
from wemake_python_styleguide.cli.commands.explain.command import ExplainCommand
from wemake_python_styleguide.cli.output import BufferedStreamWriter, Writable
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
    'WPS100 (Mock)\ndocstring\nSee at website: https://pyflak.es/WPS100'
)


def test_formatter():
    """Test that formatter formats violations as expected."""
    formatted = message_formatter.format_violation(violation_mock)
    assert formatted == violation_string


class MockWriter(Writable):
    """Writer for testing."""

    def __init__(self):
        """Create writer."""
        self.out = ''
        self.err = ''

    def write_out(self, *args) -> None:
        """Write stdout."""
        self.out += ' '.join(map(str, args))

    def write_err(self, *args) -> None:
        """Write stderr."""
        self.err += ' '.join(map(str, args))

    def flush(self) -> None:
        """Blank method. Flushing not needed."""


class MockArgs:
    """Arguments for explain command."""

    def __init__(self, code):
        """Create mock explain arguments."""
        self.violation_code = code


def test_command(snapshot):
    """Test that command works and formats violations as expected."""
    writer = MockWriter()
    command = ExplainCommand(writer)
    command.run(MockArgs('WPS123'))
    assert writer.out == snapshot


class MockBufferedStringIO(TextIO):
    """IO for testing BufferedStreamWriter."""

    def __init__(self):
        """Create IO."""
        self._buffer = BytesIO()

    @property
    def buffer(self):
        """Get IO buffer."""
        return self._buffer

    def flush(self):
        """Flush buffer."""
        self._buffer.flush()

    def writable(self):
        """Is IO writable."""
        return True

    def write(self, text):
        """Write into buffer."""
        self._buffer.write(text.encode())

    def get_string(self) -> str:
        """Get string value written into buffer."""
        return self._buffer.getvalue().decode()


def test_buffered_stream_writer():
    """Test that stream writer works as expected."""
    io_out = MockBufferedStringIO()
    io_err = MockBufferedStringIO()
    writer = BufferedStreamWriter(io_out, io_err)
    writer.write_out('Test', 'text')
    writer.write_err('Test', 'error')
    writer.flush()
    assert io_out.get_string() == 'Test text\n'
    assert io_err.get_string() == 'Test error\n'
