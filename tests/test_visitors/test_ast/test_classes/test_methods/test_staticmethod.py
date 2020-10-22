import pytest

from wemake_python_styleguide.violations.oop import StaticMethodViolation
from wemake_python_styleguide.visitors.ast.classes import WrongMethodVisitor

decorated_method = """
class Example(object):
    @{0}
    def should_fail(arg1): ...
"""


def test_staticmethod_used(
    assert_errors,
    parse_ast_tree,
    default_options,
    mode,
):
    """Testing that some built-in functions are restricted as decorators."""
    tree = parse_ast_tree(mode(decorated_method.format('staticmethod')))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [StaticMethodViolation])


@pytest.mark.parametrize('decorator', [
    'classmethod',
    'custom',
    'with_params(12, 100)',
])
def test_regular_decorator_used(
    assert_errors,
    parse_ast_tree,
    decorator,
    default_options,
    mode,
):
    """Testing that other decorators are allowed."""
    tree = parse_ast_tree(mode(decorated_method.format(decorator)))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
