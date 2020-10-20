# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    RawStringNotNeededViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongStringTokenVisitor,
)


@pytest.mark.parametrize('raw_strings', [
    r"r'some text\\'",
    r"r'some text\''",
    r"r'some text\"'",
    r'r"some text\'"',
    r"r'some text\t'",
    r"r'some text\a'",
    r"r'some text\n'",
    r"r'some text\u041b'",
    r"r'some text\043'",
    r"r'some text\x23'",
])
def test_necessary_raw_string(
    parse_tokens,
    assert_errors,
    default_options,
    raw_strings,
):
    """Ensures that correct usage of raw string works."""
    file_tokens = parse_tokens(raw_strings)

    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('raw_strings', [
    "r'No escaped character'",
    'r"Here neither"',
    "r'''Not here as well'''",
    'r"""Not here as well"""',
])
def test_unnecessary_raw_string(
    parse_tokens,
    assert_errors,
    default_options,
    raw_strings,
):
    """Ensures that usage of raw string is forbidden if no backslash."""
    file_tokens = parse_tokens(raw_strings)

    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [RawStringNotNeededViolation])
