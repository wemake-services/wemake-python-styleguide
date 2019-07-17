# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    WrongBaseClassViolation,
)
from wemake_python_styleguide.visitors.ast.classes import WrongClassVisitor

class_with_base = """
class Meta({0}):
    '''Docs.'''
"""


@pytest.mark.parametrize('base', [
    '(lambda: object)()',
    'method.call()',
    '-Name',
    '[1, 2, 3]',
])
def test_base_class_expression(
    assert_errors,
    parse_ast_tree,
    base,
    default_options,
):
    """Testing that it is not possible to use any incorrect nodes as bases."""
    tree = parse_ast_tree(class_with_base.format(base))

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongBaseClassViolation])


@pytest.mark.parametrize('base', [
    'RawName',
    'Name.Attribute',
    'Deep.Nested.Attr',
    'One, Two',
    'One, keyword=None',

    # Regressions, see: issue-459
    'Generic[ValueType]',
    'Monad[ValueType, ErrorType]',
    'Generic[Some], metaclass=abc.ABCMeta',
    'Generic["TextType"]',
])
def test_correct_base_classes(
    assert_errors,
    parse_ast_tree,
    base,
    default_options,
):
    """Testing that it is possible to use correct nodes as bases."""
    tree = parse_ast_tree(class_with_base.format(base))

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
