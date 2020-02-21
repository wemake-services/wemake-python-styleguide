# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    NonUniqueItemsInHashViolation,
)
from wemake_python_styleguide.visitors.ast.builtins import (
    WrongCollectionVisitor,
)

set_literal_template = '{{{0}, {1}}}'
nested_set_template = """
{{
    *{{
        {0},
        {1},
    }},
}}
"""

dict_literal_template = '{{ {0}: 1, {1}: 2 }}'
regression769 = '{{ **{0}, **{1} }}'


@pytest.mark.parametrize('code', [
    set_literal_template,
    nested_set_template,
    dict_literal_template,
])
@pytest.mark.parametrize('element', [
    'call()',
    '-call()',
    'some.attribute',
    '--some.attribute',
    'method.call()',
    '~method.call()',
    'some["key"]',
    '(9, function())',
    '1 + 2',  # no addition will be performed
])
def test_collection_with_impure(
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
    nested_set_template,
    dict_literal_template,
    regression769,
])
@pytest.mark.parametrize('element', [
    '1',
    '-1',
    '1 - b',
    'variable_name',
    'True',
    'None',
    'some.attr',
    'some.method()',
    'some["key"]',
    '"a" + "b"',
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
    nested_set_template,
    dict_literal_template,
])
@pytest.mark.parametrize('element', [
    '1',
    '-1',
    'variable_name',
    'True',
    'None',
    "b'1a'",
    '"string."',
    '(9, "0")',
    '3 + 1j',
    '-3 - 1j',
])
def test_collection_with_pure_duplicate(
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

    assert_errors(visitor, [NonUniqueItemsInHashViolation])


@pytest.mark.parametrize('code', [
    set_literal_template,
    nested_set_template,
])
@pytest.mark.parametrize('element', [
    '*[1, 2, 3, None]',
    '*()',
    '*{True, False, None}',
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

    assert_errors(visitor, [NonUniqueItemsInHashViolation])


@pytest.mark.parametrize('code', [
    set_literal_template,
    nested_set_template,
])
@pytest.mark.parametrize(('first', 'second'), [
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

    assert_errors(visitor, [NonUniqueItemsInHashViolation])
