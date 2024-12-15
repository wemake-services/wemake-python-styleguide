import io
import tokenize
from pathlib import Path
from textwrap import dedent

import pytest


@pytest.fixture(scope='session')
def parse_tokens(compile_code):
    """Parses tokens from a string."""

    def factory(
        code: str,
        *,
        do_compile: bool = True,
    ) -> list[tokenize.TokenInfo]:
        code = dedent(code)
        if do_compile:
            compile_code(code)
        lines = io.StringIO(code)
        return list(tokenize.generate_tokens(lambda: next(lines)))

    return factory


@pytest.fixture(scope='session')
def parse_file_tokens(parse_tokens, compile_code):
    """Parses tokens from a file."""

    def factory(
        filename: str,
        *,
        do_compile: bool = True,
    ) -> list[tokenize.TokenInfo]:
        file_content = Path(filename).read_text(encoding='utf-8')
        if do_compile:
            compile_code(file_content)
        return parse_tokens(file_content)

    return factory
