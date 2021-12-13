import pytest

from wemake_python_styleguide.violations.oop import UnpackingKwargsViolation
from wemake_python_styleguide.visitors.ast.classes import WrongClassDefVisitor

class_with_kwargs = """
class Example(BaseTestClass, {0}):
    '''Docs.'''
"""


@pytest.mark.parametrize('kwargs', ['a=1'])
def test_explicit_kwargs(
    assert_errors,
    parse_ast_tree,
    kwargs,
    default_options,
):
    """Testing keyword parameters passing."""
    tree = parse_ast_tree(class_with_kwargs.format(kwargs))

    visitor = WrongClassDefVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('kwargs', ['**kwargs'])
def test_unpacking_kwargs(
    assert_errors,
    parse_ast_tree,
    kwargs,
    default_options,
):
    """Testing that implicit kwargs unpacking is forbidden."""
    tree = parse_ast_tree(class_with_kwargs.format(kwargs))

    visitor = WrongClassDefVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnpackingKwargsViolation])
