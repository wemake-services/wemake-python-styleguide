import pytest

from wemake_python_styleguide.violations.best_practices import (
    RedundantTernaryViolation,
)
from wemake_python_styleguide.visitors.ast.redundancy import (
    RedundantTernaryVisitor,
)

# Correct:
correct_ternary_elipses = """
a if ... else c
"""

correct_not_equal = """
a if a != b else c
"""

correct_ternary_none = """
a.split() if a is not None else None
"""

# Wrong:
wrong_ternary_same_values = """
a if ... else a
"""

wrong_ternary_useless_comparison_not_eq = """
a if a != b else b
"""
wrong_ternary_useless_comparison_eq = """
b if a == b else a
"""

wrong_ternarny_none = """
a if a is not None else None
"""


@pytest.mark.parametrize('code', [
    correct_ternary_elipses,
    correct_not_equal,
    correct_ternary_none,
])
def test_correct_ternary(
    code,
    assert_errors,
    parse_ast_tree,
    default_options,
    mode,
):
    """Ensures that correct ternary expressions are fine."""
    tree = parse_ast_tree(mode(code))

    visitor = RedundantTernaryVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_ternary_same_values,
    wrong_ternary_useless_comparison_not_eq,
    wrong_ternary_useless_comparison_eq,
    wrong_ternarny_none,
])
def test_wrong_ternary(
    code,
    assert_errors,
    parse_ast_tree,
    default_options,
    mode,
):
    """Ensures that redundant ternary expressions are forbidden."""
    tree = parse_ast_tree(mode(code))

    visitor = RedundantTernaryVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [RedundantTernaryViolation])
