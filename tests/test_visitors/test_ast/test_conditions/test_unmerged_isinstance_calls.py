import pytest

from wemake_python_styleguide.violations.refactoring import (
    UnmergedIsinstanceCallsViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import (
    BooleanConditionVisitor,
)


@pytest.mark.parametrize('code', [
    'isinstance(some, int)',
    'isinstance(some, (int, CustomType))',
    'isinstance(some, int) and isinstance(some, float)',
    'isinstance(some1, int) or isinstance(some2, float)',
    'isinstance(some, int) or other',
    'other_call(some, int) or other_call(some, float)',
    'other_call(some, int) or other_call(some)',
    'isinstance(some, int) or isinstance(some, float, extra)',
    'isinstance(x, int) and some or isinstance(x, str) or other',
])
def test_regular_isinstance_conditions(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that correct conditions work."""
    tree = parse_ast_tree(code)

    visitor = BooleanConditionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    'isinstance(some, int) or isinstance(some, str)',
    'isinstance(x, int) or isinstance(x, Custom)',
    'm or isinstance(x, int) or isinstance(x, Custom)',
    'isinstance(x, int) or isinstance(x, str) or other',
    'isinstance(x, int) or other or isinstance(x, str)',
])
def test_wrong_isinstance_conditions(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that correct conditions work."""
    tree = parse_ast_tree(code)

    visitor = BooleanConditionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnmergedIsinstanceCallsViolation])
