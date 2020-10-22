import pytest

from wemake_python_styleguide.violations.refactoring import (
    ImplicitNegativeIndexViolation,
)
from wemake_python_styleguide.visitors.ast.subscripts import CorrectKeyVisitor


@pytest.mark.parametrize('code', [
    'some_list[len(some_list) - 1]',
    'some_list[len(some_list) - 1.0]',
    'some_list[len(some_list) - 5]',
    'some_list[len(some_list) - name]',
    'some_list[len(some_list) - call()]',
    'some_list[len(some_list) - name.attr]',
    'some_list[len(some_list) - name["a"]]',
    'attr.some_list[len(attr.some_list) - 1]',
])
def test_implicit_negative_index(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that implicit negative indexes are forbidden."""
    tree = parse_ast_tree(code)

    visitor = CorrectKeyVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ImplicitNegativeIndexViolation])


@pytest.mark.parametrize('code', [
    'some_list[len(other_list) - 1]',
    'some_list[len(some_list) + 1]',
    'some_list[len(some_list)]',
    'some_list[sum(some_list) + 1]',
    'some_list[len(some_list) + 1 + 2]',
    'some_list[-1]',
    'some_list[1]',
    'some_list[-name]',
    'some_list[name.attr]',
    'some_list[call() + 1]',
    'some_list[some[key]]',
])
def test_regular_len_calls(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that explicit negative calls are fine."""
    tree = parse_ast_tree(code)

    visitor = CorrectKeyVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
