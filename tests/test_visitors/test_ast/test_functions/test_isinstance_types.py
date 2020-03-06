import pytest

from wemake_python_styleguide.violations.refactoring import (
    WrongIsinstanceWithTupleViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    WrongFunctionCallVisitor,
)

isinstance_call = 'isinstance(some, {0})'


@pytest.mark.parametrize('code', [
    'int',
    '(int, float)',
    '(int, float, )',
    'call(1, 2)',
    'some.attr',
    'some.method()',
])
def test_correct_isinstance_tuple(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that isinstance is callable with correct types."""
    tree = parse_ast_tree(isinstance_call.format(code))

    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    '(int, )',
])
def test_wrong_isinstance_tuple(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that isinstance is not callable with wrong types."""
    tree = parse_ast_tree(isinstance_call.format(code))

    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongIsinstanceWithTupleViolation])
