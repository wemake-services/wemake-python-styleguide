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
    '[]',
    '(9, 0)',
    '{"key": "value"}',
    '{""}',
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
    # Strings are not checked due to strange astor representation bug
    '1',
    '-1',
    '--0.5',
    'variable_name',
    'True',
    'None',
])
def test_set_with_pure_duplicate(
    assert_errors,
    assert_error_text,
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
    assert_error_text(visitor, element)
