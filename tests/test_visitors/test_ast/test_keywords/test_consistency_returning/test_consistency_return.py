# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    InconsistentReturnViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import (
    ConsistentReturningVisitor,
)

# Correct:

correct_example1 = """
def function():
    return None
"""

correct_example2 = """
def function():
    return 'value'
"""

correct_example3 = """
def function():
    if some:
        return 1
    return None
"""

correct_example4 = """
def function():
    if some:
        return

    if other:
        return
    print()
"""

# Wrong:

wrong_example1 = """
def function():
    return
"""

wrong_example2 = """
def function():
    if some:
        return
    return None
"""

wrong_example3 = """
def function():
    if some:
        return

    if other:
        return
    print()
    return
"""

double_wrong_return = """
def function():
    if some:
        return None

    return
"""


@pytest.mark.parametrize('code', [
    wrong_example1,
    wrong_example2,
    wrong_example3,
])
def test_wrong_return_statement(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing incorrect `return` statements."""
    tree = parse_ast_tree(mode(code))

    visitor = ConsistentReturningVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [InconsistentReturnViolation])


def test_douple_wrong_return_statement(
    assert_errors,
    parse_ast_tree,
    default_options,
    mode,
):
    """Testing double incorrect `return` statements."""
    tree = parse_ast_tree(mode(double_wrong_return))

    visitor = ConsistentReturningVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        InconsistentReturnViolation,
        InconsistentReturnViolation,
    ])


@pytest.mark.parametrize('code', [
    correct_example1,
    correct_example2,
    correct_example3,
    correct_example4,
])
def test_correct_return_statements(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing correct `return` statements."""
    tree = parse_ast_tree(mode(code))

    visitor = ConsistentReturningVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
