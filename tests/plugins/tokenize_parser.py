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
