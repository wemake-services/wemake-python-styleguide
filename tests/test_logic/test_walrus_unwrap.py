# -*- coding: utf-8 -*-

import sys

import pytest

from wemake_python_styleguide.compat.constants import PY38
from wemake_python_styleguide.compat.nodes import NamedExpr
from wemake_python_styleguide.logic.walrus import get_assigned_expr


@pytest.mark.parametrize('code', [
    pytest.param(
        '(x := call())',
        marks=pytest.mark.skipif(not PY38, reason='walrus appeared in 3.8'),
    ),
    pytest.param(
        '(x := 1)',
        marks=pytest.mark.skipif(not PY38, reason='walrus appeared in 3.8'),
    ),
])
def test_get_assigned_expr(code, parse_ast_tree):
    """Returns the value of NamedExpr, the node itself otherwise."""
    node = parse_ast_tree(code)

    result_node = get_assigned_expr(node.body[0].value)

    assert isinstance(result_node, NamedExpr)


@pytest.mark.parametrize('code', [
    'x = 1',
    '"a"',
    'def some(): ...',
    'if other: ...',
    'pass',
])
def test_get_regular_node(code, parse_ast_tree):
    """Returns the value of NamedExpr, the node itself otherwise."""
    node = parse_ast_tree(code)

    result_node = get_assigned_expr(node.body[0].value)

    assert not isinstance(result_node, NamedExpr)
