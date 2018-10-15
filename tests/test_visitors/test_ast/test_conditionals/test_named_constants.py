# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    NamedConstantConditionalViolation,
)
from wemake_python_styleguide.visitors.ast.conditionals import (
    NamedConstantConditionalVisitor,
)

if_statement = """
variable = 1
if {0}:
    print('test')
"""


@pytest.mark.parametrize('code', [
    if_statement,
])
@pytest.mark.parametrize('comparators', [
    ('variable < 3'),
    ('variable'),
    ('variable is True'),
    ('variable is False'),
    ('variable is None'),
    ('variable is int or not None'),
])
def test_valid_conditional(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
):
    """Testing that conditionals work well."""
    tree = parse_ast_tree(code.format(comparators))

    visitor = NamedConstantConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    if_statement,
])
@pytest.mark.parametrize('comparators', [
    'True',
    'False',
    'None',
])
def test_redundant(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
):
    """Testing that violations are when comparing identical variable."""
    tree = parse_ast_tree(code.format(comparators))

    visitor = NamedConstantConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NamedConstantConditionalViolation])
