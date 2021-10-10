import pytest

from wemake_python_styleguide.violations.best_practices import (
    KwargsUnpackingInClassDefinitionViolation,
)
from wemake_python_styleguide.visitors.ast.classes import WrongClassVisitor

class_definition_with_unpacking_one = """
kwargs = {'some_arg': 'some_arg'}
class TestClass(object, **kwargs):
    '''Docs.'''
"""

class_definition_with_unpacking_two = """
class TestClass(object, **{}):
    '''Docs.'''
"""  # noqa: P103

class_definition_with_unpacking_and_arguments = """
kwargs = {'another_arg': 'another_arg'}
class TestClass(object, some_arg='some_arg', **kwargs):
    '''Docs.'''
"""


@pytest.mark.parametrize('code', [
    class_definition_with_unpacking_one,
    class_definition_with_unpacking_two,
    class_definition_with_unpacking_and_arguments,
])
def test_kwarg_unpacking_violation(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that it is not possible to unpack values in class definition."""
    tree = parse_ast_tree(code)

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [KwargsUnpackingInClassDefinitionViolation])


class_definition_with_keyword_arg = """
class TestClass(object, some_arg='some_arg'):
    '''Docs.'''
"""


@pytest.mark.parametrize('code', [
    class_definition_with_keyword_arg,
])
def test_kwarg_unpacking_violation_except(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that is possible to pass kw arguments in class definition."""
    tree = parse_ast_tree(code)

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
