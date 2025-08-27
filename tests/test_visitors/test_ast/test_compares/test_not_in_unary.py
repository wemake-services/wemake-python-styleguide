import pytest

from wemake_python_styleguide.violations.consistency import (
    NotInWithUnaryOpViolation,
)
from wemake_python_styleguide.visitors.ast.compares import (
    NotInUnaryVisitor,
)


@pytest.mark.parametrize(
    'code',
    [
        'if not x in items: ...',
        'if not (x in items): ...',
        'result = not value in data',
        'flag = not (value in data)',
        'while not a in b: ...',
    ],
)
def test_not_in_unary_detects(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Ensures that ``not a in b`` forms are reported."""
    tree = parse_ast_tree(code)

    visitor = NotInUnaryVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NotInWithUnaryOpViolation])


@pytest.mark.parametrize(
    'code',
    [
        'if x not in items: ...',
        'result = x not in data',
        'if (not x) in items: ...',
        'if not_called() in seq: ...',
        'if y in items: ...',
        'if not a is b: ...',
        'if not (a is b): ...',
        'if not (x in y in z): ...',
    ],
)
def test_not_in_unary_ok(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Ensures that correct forms are not reported."""
    tree = parse_ast_tree(code)

    visitor = NotInUnaryVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
