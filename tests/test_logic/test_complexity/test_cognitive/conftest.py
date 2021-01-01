"""
Fixtures to make testing cognitive complexity easy.

Policy for testing cognitive complexity:

1. Use a single function def in code samples
2. Write ``# +x`` comments on each line where addition happens

Adapted from https://github.com/Melevir/cognitive_complexity
"""

import ast

import pytest

from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.logic.complexity import cognitive


def _find_function(tree: ast.AST):
    for node in ast.walk(tree):
        if isinstance(node, FunctionNodes):
            return node
    return None


@pytest.fixture(scope='session')
def get_code_snippet_complexity(parse_ast_tree):
    """Fixture to parse and count cognitive complexity the easy way."""
    def factory(src: str) -> int:
        funcdef = _find_function(parse_ast_tree(src))
        assert funcdef, 'No function definition found'
        return cognitive.cognitive_score(funcdef)
    return factory
