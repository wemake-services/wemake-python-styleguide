import pytest

from wemake_python_styleguide.violations.oop import BuiltinSubclassViolation
from wemake_python_styleguide.visitors.ast.classes import WrongClassDefVisitor

class_with_base = """
class TestClass({0}):
    '''Docs.'''
"""


@pytest.mark.parametrize('super_class', [
    'int',
    'str',
    'bool',
    'list',
    'dict',
    'float',
])
def test_builtin_subclass(
    assert_errors,
    parse_ast_tree,
    super_class,
    default_options,
):
    """Testing that it is not possible to subclass builtins."""
    tree = parse_ast_tree(class_with_base.format(super_class))

    visitor = WrongClassDefVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BuiltinSubclassViolation])


@pytest.mark.parametrize('super_class', [
    'type',
    'object',
    'Custom',
    'Multiple, Classes',
])
def test_regular_subclass(
    assert_errors,
    parse_ast_tree,
    super_class,
    default_options,
):
    """Testing that it is possible to subclass regulars."""
    tree = parse_ast_tree(class_with_base.format(super_class))

    visitor = WrongClassDefVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
