# -*- coding: utf-8 -*-

import sys

import pytest

from wemake_python_styleguide.compat.constants import PY38
from wemake_python_styleguide.logic.walrus import get_assigned_expr


@pytest.mark.parametrize('code', [
    'x = 1',
    pytest.param(
        '(x := 1)',
        marks=pytest.mark.skipif(
            sys.version_info < (3, 8),
            reason='NamedExpr appeared in 3.8',
        ),
    ),
])
def test_get_assigned_expr(code, parse_ast_tree):
    """Returns the value of NamedExpr, the node itself otherwise."""
    node = parse_ast_tree(code)
    result_node = get_assigned_expr(node.body[0].value)
    if PY38:
        assert result_node.value == 1
    else:
        assert result_node.n == 1
