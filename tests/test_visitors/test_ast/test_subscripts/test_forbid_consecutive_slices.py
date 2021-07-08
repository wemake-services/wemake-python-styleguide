import pytest

from wemake_python_styleguide.violations.consistency import (
    ForbidConsecutiveSlicesViolation,
)
from wemake_python_styleguide.visitors.ast.subscripts import (
    ConsecutiveSlicesVisitor,
)

no_consecutive = """
a = [1, 2, 3, 4]
b = a[1:]
"""

no_consecutive_fslice = """
a = [1, 2, 3, 4]
b = a[1:][2]
"""

no_consecutive_sslice = """
a = [1, [2, 3, 4, 5], 3, 4]
b = a[1][2:]
"""

no_slicing = """
a = [1, 2, 3, 4]
b = a[1]
"""

no_slicing_double = """
a = [1, [5, 6, 7], 3, 4]
b = a[1][3]
"""

no_slicing_triple = """
a = [1, [5, 6, 7, [8, 9, 10]], 3, 4]
b = a[1][3][1]
"""

consecutive_double = """
a = [1, 2, 3, 4]
b = a[1:][2:]
"""

consecutive_triple = """
a = [1, 2, 3, 4, 5, 6]
b = a[1:][2:][:2]
"""

consecutive_plus = """
a = [1, [5, 6, 7, 8, 9, 10], 3, 4]
b = a[1][2:][:4]
"""

no_consecutive_for_slices = """
a = [1, [5, 6, 7, [8, [1, 2, 3, 4], 10]], 3, 4]
for i in a[1][3][1]:
    print(i)
"""

consecutive_for = """
a = [1, [5, 6, 7, [8, [1, 2, 3, 4], 10]], 3, 4]
for i in a[1][:4][1:]:
    print(i)
"""


@pytest.mark.parametrize('code', [
    no_consecutive,
    no_consecutive_fslice,
    no_consecutive_sslice,
    no_slicing,
    no_slicing_double,
    no_slicing_triple,
    no_consecutive_for_slices,
])
def test_no_slicing(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing cases that does not raise the violation."""
    tree = parse_ast_tree(code)
    visitor = ConsecutiveSlicesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    consecutive_double,
    consecutive_triple,
    consecutive_plus,
    consecutive_for,
])
def test_slicing(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing cases that raise the violation."""
    tree = parse_ast_tree(code)
    visitor = ConsecutiveSlicesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ForbidConsecutiveSlicesViolation])
