import pytest

from wemake_python_styleguide.violations.best_practices import (
    RedundantTernaryViolation,
)
from wemake_python_styleguide.visitors.ast.redundancy import (
    RedundantTernaryVisitor,
)

# Correct:
correct_not_equal = """
a if a != b else c
"""

# Wrong:
wrong_ternary_useless_comparison_not_eq = """
a if a != b else b
"""
wrong_ternary_useless_comparison_eq = """
b if a == b else a
"""


@pytest.mark.parametrize('code', [
    correct_not_equal,
])
def test_correct_ternary(
    code,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Ensures that correct ternary expressions are fine."""
    tree = parse_ast_tree(code)

    visitor = RedundantTernaryVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_ternary_useless_comparison_not_eq,
    wrong_ternary_useless_comparison_eq,
])
def test_wrong_ternary(
    code,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Ensures that redundant ternary expressions are forbidden."""
    tree = parse_ast_tree(code)

    visitor = RedundantTernaryVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [RedundantTernaryViolation])
