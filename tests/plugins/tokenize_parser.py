# -*- coding: utf-8 -*-

import io
import tokenize
from textwrap import dedent

import pytest


@pytest.fixture(scope='session')
def parse_tokens():
    """Parses tokens from a string."""
    def factory(code: str):
        lines = io.StringIO(dedent(code))
        return list(tokenize.generate_tokens(lambda: next(lines)))
    return factory


@pytest.fixture(scope='session')
def parse_file_tokens():
    """Parses tokens from a file."""
    def factory(filename: str):
        with open(filename, 'r', encoding='utf-8') as test_file:
            file_content = test_file.read()
            lines = io.StringIO(dedent(file_content))
            return list(tokenize.generate_tokens(lambda: next(lines)))
    return factory
