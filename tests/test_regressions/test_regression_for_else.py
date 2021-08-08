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


def test_regression_for_else(
    assert_errors,
    default_options,
    parse_ast_tree,
):
    """Tests for nested ``if`` statement in ``for else`` statement."""
    tree = parse_ast_tree(code_that_breaks)

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ValueError])
