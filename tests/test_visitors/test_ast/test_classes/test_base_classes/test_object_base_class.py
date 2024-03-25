import pytest

from wemake_python_styleguide.violations.consistency import (
    ExplicitObjectBaseClassViolation,
)
from wemake_python_styleguide.visitors.ast.classes import WrongClassDefVisitor
from wemake_python_styleguide.compat.constants import PY312

skip_pep695 = pytest.mark.skipif(not PY312, reason='PEP 695 was added in 3.12')

# Correct:

class_without_base = """
class Meta:
    '''Docs.'''
"""

class_with_empty_base = """
class Meta():
    '''Docs.'''
"""

nested_class_without_base = """
class Model:
    class Meta:
        '''Docs.'''
"""

nested_class_with_empty_base = """
class Model:
    class Meta():
        '''Docs.'''
"""

class_pep695 = """
class Base[Type]:
   some_attr: Type
"""

# Wrong:

class_with_base = """
class Meta({0}):
    '''Docs.'''
"""

nested_class_with_base = """
class Model:
    class Meta({0}):
        '''Docs.'''
"""

class_pep695_with_base = """
class Meta[Type]({0}):
   some_attr: Type
"""


@pytest.mark.parametrize('code', [
    class_without_base,
    class_with_empty_base,
    nested_class_without_base,
    nested_class_with_empty_base,
    pytest.param(
        class_pep695,
        marks=skip_pep695,
    ),
])
def test_no_base_class(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing no explicit base class is allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongClassDefVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    class_with_base,
    nested_class_with_base,
    pytest.param(
        class_pep695_with_base,
        marks=skip_pep695,
    ),
])
@pytest.mark.parametrize('base', [
    'type',
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


@pytest.mark.parametrize('code', [
    class_with_base,
    nested_class_with_base,
    pytest.param(
        class_pep695_with_base,
        marks=skip_pep695,
    ),
])
def test_forbidden_object_base_class(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that `object` base class is forbidden."""
    tree = parse_ast_tree(code.format('object'))

    visitor = WrongClassDefVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ExplicitObjectBaseClassViolation])
    assert_error_text(visitor, 'Meta')
