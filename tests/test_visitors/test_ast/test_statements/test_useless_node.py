# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    UselessNodeViolation,
)
from wemake_python_styleguide.visitors.ast.statements import (
    StatementsWithBodiesVisitor,
)

for_template = """
def wrapper():
    for some_var in call():
        {0}
"""

while_template = """
def wrapper():
    while True:
        {0}
"""

with_template = """
def wrapper():
    for wrapping_loop in []:
        with some():
            {0}
"""

try_template = """
def wrapper():
    for wrapping_loop in []:
        try:
            {0}
        except Exception:
            some_call()
"""


@pytest.mark.parametrize('code', [
    for_template,
    while_template,
    with_template,
    try_template,
])
@pytest.mark.parametrize('statement', [
    'break',
    'continue',
    'pass',
])
def test_useless_nodes(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
    mode,
):
    """Ensures that useless nodes are forbidden."""
    tree = parse_ast_tree(mode(code.format(statement)))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessNodeViolation])


@pytest.mark.parametrize('code', [
    for_template,
    while_template,
])
@pytest.mark.parametrize('statement', [
    'return 1',
    'raise TypeError()',
])
def test_useless_loop_nodes(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
    mode,
):
    """Ensures that useless loop nodes are forbidden."""
    tree = parse_ast_tree(mode(code.format(statement)))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessNodeViolation])


@pytest.mark.parametrize('code', [
    try_template,
])
@pytest.mark.parametrize('statement', [
    'raise TypeError()',
])
def test_useless_try_nodes(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
    mode,
):
    """Ensures that useless try nodes are forbidden."""
    tree = parse_ast_tree(mode(code.format(statement)))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessNodeViolation])


@pytest.mark.parametrize('code', [
    for_template,
    while_template,
    with_template,
    try_template,
])
@pytest.mark.parametrize('statement', [
    'some_var = 1',
    'some_call()',
])
def test_useful_nodes(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
    mode,
):
    """Ensures that useful nodes are required."""
    tree = parse_ast_tree(mode(code.format(statement)))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
