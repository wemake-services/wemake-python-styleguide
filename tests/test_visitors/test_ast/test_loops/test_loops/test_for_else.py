import pytest

from wemake_python_styleguide.visitors.ast.conditions import IfStatementVisitor

code_that_breaks = """
def is_prime(number: int):
    for i in range(2, number):
        if number % i == 0:
            return False
    else:
        if number != 1:
            return True
    return False
"""

code_that_works = """
def is_prime(number: int):
    for i in range(2, number):
        if number % i == 0:
            return False
"""

code_with_complex_if = """
def _has_same_args(
    node,
    call,
):
    for num in node:
        if num:
            if isinstance(num, int):
                return False
        elif isinstance(num, str):
            if num > 2:
                return False
        else:
            return False
    return True
"""


@pytest.mark.parametrize('code', [
    code_that_breaks,
    code_that_works,
    code_with_complex_if,
])
def test_regression_for_else(
    assert_errors,
    default_options,
    parse_ast_tree,
    code,
):
    """Tests for nested ``if`` statement in ``for else`` statement."""
    tree = parse_ast_tree(code)

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
