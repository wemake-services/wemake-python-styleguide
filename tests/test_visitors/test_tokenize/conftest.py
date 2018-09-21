# -*- coding: utf-8 -*-

import tokenize
from io import BytesIO
from textwrap import dedent

import pytest


@pytest.fixture(scope='session')
def parse_tokens():
    """Parses tokens from a string."""
    def factory(code: str):
        buffer = BytesIO(dedent(code).encode('utf-8'))
        return list(tokenize.tokenize(buffer.readline))
    return factory
