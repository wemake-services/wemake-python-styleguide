import pytest

from wemake_python_styleguide.constants import MAGIC_METHODS_BLACKLIST
from wemake_python_styleguide.violations.oop import BadMagicMethodViolation
from wemake_python_styleguide.visitors.ast.classes import WrongMethodVisitor

magic_method = """
class Example(object):
    def {0}(self): ...
"""

regular_function = 'def {0}(): ...'


@pytest.mark.parametrize('method', MAGIC_METHODS_BLACKLIST)
def test_wrong_magic_used(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    method,
    default_options,
):
    """Testing that some magic methods are restricted."""
    tree = parse_ast_tree(magic_method.format(method))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BadMagicMethodViolation])
    assert_error_text(visitor, method)


@pytest.mark.parametrize('code', [
    magic_method,
    regular_function,
])
@pytest.mark.parametrize('method', [
    '__add__',
    '__init__',
])
def test_correct_magic_method_used(
    assert_errors,
    parse_ast_tree,
    code,
    method,
    default_options,
):
    """Testing that some magic methods are working fine."""
    tree = parse_ast_tree(code.format(method))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    magic_method,
    regular_function,
])
@pytest.mark.parametrize('method', [
    'next',
    'regular',
])
def test_regular_method_used(
    assert_errors,
    parse_ast_tree,
    code,
    method,
    mode,
    default_options,
):
    """Testing that other methods are working fine."""
    tree = parse_ast_tree(mode(code.format(method)))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
