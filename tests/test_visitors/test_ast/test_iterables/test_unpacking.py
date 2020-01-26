# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    IterableUnpackingViolation,
)
from wemake_python_styleguide.visitors.ast.iterables import (
    IterableUnpackingVisitor,
)

args_unpacking_in_call = 'f(*args)'
spread_list_definition = '[1, 2, *numbers, 74]'
spread_set_definition = '{1, 2, *numbers, 74}'
spread_tuple_definition = '(1, 2, *numbers, 74)'
spread_assignment = 'first, *_ = [1, 2, 4, 3]'

wrong_list_definition = '[*numbers]'
wrong_set_definition = '{*numbers}'
wrong_tuple_definition = '(*numbers,)'
wrong_spread_assignment = '*_, = [1, 2, 4, 3]'


@pytest.mark.parametrize('code', [
    args_unpacking_in_call,
    spread_list_definition,
    spread_set_definition,
    spread_tuple_definition,
    spread_assignment,
])
def test_correct_iterable_unpacking_usage(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that correct iterable unpacking is allowed."""
    tree = parse_ast_tree(code)

    visitor = IterableUnpackingVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_list_definition,
    wrong_set_definition,
    wrong_tuple_definition,
    wrong_spread_assignment,
])
def test_unneccessary_iterable_unpacking_usage(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that unneccessary iterable unpacking is restricted."""
    tree = parse_ast_tree(code)

    visitor = IterableUnpackingVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [IterableUnpackingViolation])
