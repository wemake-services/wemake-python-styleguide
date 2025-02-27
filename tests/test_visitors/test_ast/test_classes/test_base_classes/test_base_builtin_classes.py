import pytest

from wemake_python_styleguide.violations.oop import BuiltinSubclassViolation
from wemake_python_styleguide.visitors.ast.classes.classdef import (
    WrongClassDefVisitor,
)

class_with_base = 'class TestClass({0}): ...'

enum_with_primitive1 = 'class First({0}, enum.Enum): ...'
enum_with_primitive2 = 'class First({0}, Enum): ...'
enum_with_primitive3 = 'class First({0}, EnumMeta): ...'
enum_with_primitive4 = 'class First({0}, enum.EnumType): ...'


@pytest.mark.parametrize(
    'super_class',
    [
        'int',
        'str',
        'bool',
        'list',
        'dict',
        'float',
    ],
)
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


# `object` has a special violation, not included here:
@pytest.mark.parametrize(
    'super_class',
    [
        'type',
        'Custom',
        'Multiple, Classes',
    ],
)
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


@pytest.mark.parametrize(
    'template',
    [
        enum_with_primitive1,
        enum_with_primitive2,
        enum_with_primitive3,
        enum_with_primitive4,
    ],
)
@pytest.mark.parametrize(
    'code',
    [
        'int',
        'str',
        'bool',
        'list',
        'dict',
        'float',
    ],
)
def test_builtin_subclass_with_enum(
    assert_errors,
    parse_ast_tree,
    template,
    code,
    default_options,
):
    """Testing extending `enum` is always fine with primitive."""
    tree = parse_ast_tree(template.format(code))

    visitor = WrongClassDefVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
