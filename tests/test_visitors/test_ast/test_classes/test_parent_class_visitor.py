# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    WrongParentClassListDef,
)
from wemake_python_styleguide.visitors.ast.classes import (
    WrongParentClassListVisitor,
)


@pytest.mark.parametrize('code', [
    'class TestClassName(FirstClassName, SecondClassName, object): ...',
])
def test_wrong_class_definition_multiple_parent(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing wrong class definition."""
    tree = parse_ast_tree(code)

    visitor = WrongParentClassListVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongParentClassListDef])


@pytest.mark.parametrize('code', [
    'class TestClassName(object): ...',
])
def test_correct_class_definition_single_parent(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing correct class definition with single parent."""
    tree = parse_ast_tree(code)

    visitor = WrongParentClassListVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    'class TestClassName(FirstTestClass, SecondTestClass): ...',
])
def test_correct_class_definition_multiple_parent(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing correct class definition with multiple parent."""
    tree = parse_ast_tree(code)

    visitor = WrongParentClassListVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
