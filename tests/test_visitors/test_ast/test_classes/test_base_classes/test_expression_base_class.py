# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.oop import WrongBaseClassViolation
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
    '(First, Second)',
    'None',
    'Call().attr',
    'dict[1].attr',
    'dict[1].attr()',
    'Generic[TextType][Nested]',
    'Generic["TextType"][Nested]',
    'Call()[x]',
    '[12][0]',
    '[].len',
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
    'Monad[ValueType, None]',
    'Generic[Some], metaclass=abc.ABCMeta',
    'types.Generic[X]',
    'Generic[ast.AST]',
    'Generic[Optional[int]]',
    'Generic[Literal[1]]',

    # Might be removed later:
    'Generic[1]',  # int
    'Generic["X"]',  # str
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
