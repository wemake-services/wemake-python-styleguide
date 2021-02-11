import io
import tokenize
from textwrap import dedent

import pytest


@pytest.fixture(scope='session')
def parse_tokens(compile_code):
    """Parses tokens from a string."""
    def factory(code: str, *, do_compile: bool = True) -> None:
        code = dedent(code)
        if do_compile:
            compile_code(code)
        lines = io.StringIO(code)
        return list(tokenize.generate_tokens(lambda: next(lines)))
    return factory


@pytest.fixture(scope='session')
def parse_file_tokens(parse_tokens, compile_code):
    """Parses tokens from a file."""
    def factory(filename: str, *, do_compile: bool = True) -> None:
        with open(filename, 'r', encoding='utf-8') as test_file:
            file_content = test_file.read()
            if do_compile:
                compile_code(file_content)
            return parse_tokens(file_content)
    return factory
