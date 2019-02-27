# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    ContextManagerVariableDefinitionViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import (
    WrongContextManagerVisitor,
)

context_manager_definition = """
def wrapper():
    with open('') as {0}:
        ...
"""


@pytest.mark.parametrize('code', [
    'xy[0]',
    'xy.attr',
    'xy["key"]',
    '(valid, invalid.attr)',
    '(invalid.attr, valid)',
])
def test_context_manager_wrong_definitions(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing incorrect definitions context manager assignment."""
    tree = parse_ast_tree(mode(context_manager_definition.format(code)))

    visitor = WrongContextManagerVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ContextManagerVariableDefinitionViolation])


@pytest.mark.parametrize('code', [
    'xy',
    '(valid1, valid2)',
])
def test_context_manager_correct_definitions(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing correct definitions context manager assignment."""
    tree = parse_ast_tree(mode(context_manager_definition.format(code)))

    visitor = WrongContextManagerVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
