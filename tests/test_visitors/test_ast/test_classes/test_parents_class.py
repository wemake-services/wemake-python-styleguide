# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    RedundantClassParentViolation,
)
from wemake_python_styleguide.visitors.ast.classes import WrongClassVisitor

class_with_object_only = 'class WithObjectOnly(object): ...'
class_with_multiple_parents_object_last = """
class ManyParents(Parent1, Parent2, object): ..."""
class_with_multiple_parents_object_first = """
class ManyParents(object, Parent1, Parent2): ..."""


@pytest.mark.parametrize('code', [
    class_with_multiple_parents_object_last,
    class_with_multiple_parents_object_first,
])
def test_multiple_parents_object(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that using `object` with many class parents is forbidden."""
    tree = parse_ast_tree(code)

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [RedundantClassParentViolation])


@pytest.mark.parametrize('code', [
    class_with_object_only,
])
def test_regular_base_classes(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that class with a single base class `object` is allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
