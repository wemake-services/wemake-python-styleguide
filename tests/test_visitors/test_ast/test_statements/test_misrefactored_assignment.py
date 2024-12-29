import pytest

from wemake_python_styleguide.violations.refactoring import (
    MisrefactoredAssignmentViolation,
)
from wemake_python_styleguide.visitors.ast.statements import (
    StatementsWithBodiesVisitor,
)


@pytest.mark.parametrize(
    'code',
    [
        'x += x + 2',
        'x -= x - 1',
        'x *= x * 1',
        'x /= x / 1',
        'x **= x ** 1',
        'x ^= x ^ 1',
        'x %= x % 1',
        'x >>= x >> 1',
        'x <<= x << 1',
        'x &= x & 1',
        'x |= x | 1',
        'x @= x | 1',
    ],
)
def test_misrefactored_assignment(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that misrefactored assignments detected."""
    tree = parse_ast_tree(code)

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MisrefactoredAssignmentViolation])


@pytest.mark.parametrize(
    'code',
    [
        'x += y + 2',
        'x -= 1 - y',
        'x *= x2 * 1',
        'x2 /= x / 1',
        'x **= (x - y) ** 1',
        'x ^= (x + 1) ^ 1',
        'x %= x() % 1',
        'x >>= a.x >> 1',
        'x <<= x.x << 1',
        'x &= x.x() & 1',
        'x |= (y := 2) | 1',
        'x |= -x | 1',
    ],
)
def test_correct_assignment(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that correct assignments are possible."""
    tree = parse_ast_tree(code)

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
