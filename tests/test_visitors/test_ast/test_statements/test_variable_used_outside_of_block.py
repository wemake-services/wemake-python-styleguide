# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    VariableUsedOutsideOfBlockViolation,
)
from wemake_python_styleguide.visitors.ast.statements import (
    VariableUsedOutsideOfBlockVisitor,
)

variable_used_outside_with = """
def function():
    with foo.open() as bar:
        some_call()
    print('This is not allowed'.format(bar))
"""

multiple_variables_defined_by_with = """
def test_context():
    with foo.open(), bar.open() as baz, qux.open() as (quux, quuz):
        print("Hello")
    print(quuz)
"""

variable_used_outside_for = """
def test_context():
    for ind in range(100):
        print(ind)
    total = ind + 1
"""

multiple_variables_defined_by_for = """
def test_context():
    for (foo, bar, baz, qux) in call(1):
        iterate()
    total = baz / 2
"""

valid_with_usage = """
def test_context():
    with manager as (foo, bar):
        print(bar)
    print(manager)
"""


valid_for_usage = """
def test_context():
    counter = 0
    for foo in range(100):
        print(foo)
        counter = foo
    print(counter)
"""


@pytest.mark.parametrize('example', [
    variable_used_outside_for,
    multiple_variables_defined_by_for,
    variable_used_outside_with,
    multiple_variables_defined_by_with,
])
def test_detect_violations(
    example,
    assert_errors,
    parse_ast_tree,
    default_options,
    mode,
):
    """Testing that detection of variables being used outside of block."""
    tree = parse_ast_tree(mode(example))
    visitor = VariableUsedOutsideOfBlockVisitor(default_options, tree)
    visitor.run()
    assert_errors(visitor, [VariableUsedOutsideOfBlockViolation])


@pytest.mark.parametrize('example', [
    valid_for_usage,
    valid_with_usage,
])
def test_valid_variables_usage(
    example,
    assert_errors,
    parse_ast_tree,
    default_options,
    mode,
):
    """Testing that detection of variables being used outside of block."""
    tree = parse_ast_tree(mode(example))
    visitor = VariableUsedOutsideOfBlockVisitor(default_options, tree)
    visitor.run()
    assert_errors(visitor, [])
