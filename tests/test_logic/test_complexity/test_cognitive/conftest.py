# -*- coding: utf-8 -*-

"""
Fixtures to make testing cognitive complexity easy.

Adapted from https://github.com/Melevir/cognitive_complexity
"""

import ast
import textwrap

import pytest

from wemake_python_styleguide.logic.complexity import cognitive


@pytest.fixture(scope='session')
def get_code_snippet_compexity():
    """Fixture to parse and count cognitive complexity the easy way."""
    def factory(src: str) -> int:
        funcdef = ast.parse(textwrap.dedent(src).strip()).body[0]
        return cognitive.cognitive_score(funcdef)
    return factory
