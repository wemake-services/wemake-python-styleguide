# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    NonUniqueItemsInSetViolation,
)
from wemake_python_styleguide.visitors.ast.builtins import (
    WrongCollectionVisitor,
)

set_literal_template = '{{{0}, {1}}}'


@pytest.mark.parametrize('code', [
    set_literal_template,
])
@pytest.mark.parametrize('element', [
    'call()',
    '-call()',
    'some.attribute',
    '--some.attribute',
    'method.call()',
    '~method.call()',
    'some["key"]',
    '[item.call()]',
    '(9, function())',
    '{"key": some_value.attr}',
    '{some_value.attr, some_other}',
    '*[item2["access"]]',
    '1 + 2',  # no addition will be performed
])
def test_set_with_impure(
    assert_errors,
    parse_ast_tree,
    code,
    element,
    default_options,
):
    """Testing that impure elements can be contained in set multiple times."""
    tree = parse_ast_tree(code.format(element, element))

    visitor = WrongCollectionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    set_literal_template,
])
@pytest.mark.parametrize('element', [
    '1',
    '-1',
    '0.5',
    'variable_name',
    'True',
    'None',
    'some.attr',
    'some.method()',
    'some["key"]',
])
def test_set_with_pure_unique(
    assert_errors,
    parse_ast_tree,
    code,
    element,
    default_options,
):
    """Testing that unique elements are allowed."""
    tree = parse_ast_tree(code.format(element, 'other'))

    visitor = WrongCollectionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    set_literal_template,
])
@pytest.mark.parametrize('element', [
    '1',
    '-1',
    '--0.5',
    'variable_name',
    'True',
    'None',
    "b'1a'",
    '"string."',
    '[]',
    '[name, name2]',
    '(9, "0")',
    "{'key': value}",
    "{'', '1', True}",
    '*[1, 2, 3, None]',
    '*()',
    '3 + 1j',
    '-3 - 1j',
])
def test_set_with_pure_duplicate(
    assert_errors,
    parse_ast_tree,
    code,
    element,
    default_options,
):
    """Testing that pure elements can not be contained multiple times."""
    tree = parse_ast_tree(code.format(element, element))

    visitor = WrongCollectionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NonUniqueItemsInSetViolation])


@pytest.mark.parametrize('code', [
    set_literal_template,
])
@pytest.mark.parametrize('first, second', [
    ('1', 'True'),
    ('1', '1.0'),
    ('-1', '-1.0'),
    ('1.0', 'True'),
    ('-0', '-False'),
    ('0.0', 'False'),
])
def test_set_with_similar_values(
    assert_errors,
    parse_ast_tree,
    code,
    first,
    second,
    default_options,
):
    """Testing that same values are reported."""
    tree = parse_ast_tree(code.format(first, second))

    visitor = WrongCollectionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NonUniqueItemsInSetViolation])
