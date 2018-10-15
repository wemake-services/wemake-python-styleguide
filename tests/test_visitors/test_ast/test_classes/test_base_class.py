# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    RequiredBaseClassViolation,
)
from wemake_python_styleguide.visitors.ast.classes import WrongClassVisitor

class_without_base = 'class WithoutBase: ...'
class_with_empty_base = 'class EmptyBase(): ...'

nested_class_without_base = """
class Model(object):
    class Meta: ...
"""

nested_class_with_empty_base = """
class Model(object):
    class Meta(): ...
"""

# Correct:

class_with_base = 'class Example({0}): ...'

nested_class_with_base = """
class Model({0}):
    class Meta({0}): ...
"""


@pytest.mark.parametrize('code', [
    class_without_base,
    class_with_empty_base,
    nested_class_without_base,
    nested_class_with_empty_base,
])
def test_wrong_base_class(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that not using explicit base class is forbidden."""
    tree = parse_ast_tree(code)

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [RequiredBaseClassViolation])


@pytest.mark.parametrize('code', [
    class_with_base,
    nested_class_with_base,
])
@pytest.mark.parametrize('base', [
    'type',
    'object',
    'dict',
    'CustomClass',
    'Multiple, Classes, Mixins',
    'Custom, keyword=1',
])
def test_regular_base_classes(
    assert_errors,
    parse_ast_tree,
    code,
    base,
    default_options,
):
    """Testing that regular base classes work."""
    tree = parse_ast_tree(code.format(base))

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
