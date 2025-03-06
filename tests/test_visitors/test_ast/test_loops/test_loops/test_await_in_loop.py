import pytest

from wemake_python_styleguide.violations.best_practices import (
    AwaitInLoopViolation,
)
from wemake_python_styleguide.visitors.ast.loops import WrongLoopVisitor

code_that_breaks = """
async def foo():
    for _ in range(1):
        await some()
"""


@pytest.mark.parametrize(
    'code',
    [
        code_that_breaks,
    ],
)
def test_await_statement_in_for_loop(
    assert_errors,
    default_options,
    parse_ast_tree,
    code,
):
    """Tests for nested ``await`` statement in ``for`` loop."""
    tree = parse_ast_tree(code)

    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [AwaitInLoopViolation])
