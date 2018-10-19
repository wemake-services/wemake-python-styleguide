# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    WrongParentClassListDef,
)
from wemake_python_styleguide.visitors.ast.classes import WrongClassVisitor

extra_object = 'class TestClassName(FirstName, SecondName, object): ...'


@pytest.mark.parametrize('code', [
    extra_object,
])
def test_wrong_class_definition_multiple_parent(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing wrong class definition."""
    tree = parse_ast_tree(code)

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongParentClassListDef])


single_extra_object = 'class TestClassName(object): ...'
correct_list = 'class TestClassName(FirstTestClass, SecondTestClass): ...'


@pytest.mark.parametrize('code', [
    single_extra_object,
    correct_list,
])
def test_correct_class_definitions(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing correct class definition with single parent."""
    tree = parse_ast_tree(code)

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
