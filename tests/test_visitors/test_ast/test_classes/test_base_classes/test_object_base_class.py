import pytest

from wemake_python_styleguide.violations.consistency import (
    RequiredBaseClassViolation,
)
from wemake_python_styleguide.visitors.ast.classes import WrongClassDefVisitor

class_without_base = """
class Meta:
    '''Docs.'''
"""

class_with_empty_base = """
class Meta():
    '''Docs.'''
"""

nested_class_without_base = """
class Model(object):
    class Meta:
        '''Docs.'''
"""

nested_class_with_empty_base = """
class Model(object):
    class Meta():
        '''Docs.'''
"""

# Correct:

class_with_base = """
class Meta({0}):
    '''Docs.'''
"""

nested_class_with_base = """
class Model({0}):
    class Meta({0}):
        '''Docs.'''
"""


@pytest.mark.parametrize('code', [
    class_without_base,
    class_with_empty_base,
    nested_class_without_base,
    nested_class_with_empty_base,
])
def test_wrong_base_class(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that not using explicit base class is forbidden."""
    tree = parse_ast_tree(code)

    visitor = WrongClassDefVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [RequiredBaseClassViolation])
    assert_error_text(visitor, 'Meta')


@pytest.mark.parametrize('code', [
    class_with_base,
    nested_class_with_base,
])
@pytest.mark.parametrize('base', [
    'type',
    'object',
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

    visitor = WrongClassDefVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
