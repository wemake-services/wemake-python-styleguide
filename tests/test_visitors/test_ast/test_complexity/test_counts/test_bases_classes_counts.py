# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.complexity import (
    TooManyBaseClassesViolation,
)
from wemake_python_styleguide.visitors.ast.classes import WrongClassVisitor

correct_count = """
   class CorrectClassName(FirstParentClass,
              SecondParentClass,
              ThirdParentClass): ...
"""


@pytest.mark.parametrize('code', [
    correct_count,
])
def test_correct_count(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing of correct base classes number."""
    tree = parse_ast_tree(code)

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


too_many_count = """
   class SomeClassName(FirstParentClass,
              SecondParentClass,
              ThirdParentClass,
              CustomClass,
              AddedClass): ...
"""


@pytest.mark.parametrize('code', [
    too_many_count,
])
def test_bad_number_default_option(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing of base classes number with default options."""
    tree = parse_ast_tree(code)

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyBaseClassesViolation])


@pytest.mark.parametrize('code', [
    too_many_count,
    correct_count,
])
def test_bad_number_custom_option(
    assert_errors, parse_ast_tree, code, options,
):
    """Testing of base classes number with custom options."""
    tree = parse_ast_tree(code)

    options = options(max_classes_number=5)
    visitor = WrongClassVisitor(options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
