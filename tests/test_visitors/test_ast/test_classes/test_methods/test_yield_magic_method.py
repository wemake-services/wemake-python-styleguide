import pytest

from wemake_python_styleguide.violations.oop import YieldMagicMethodViolation
from wemake_python_styleguide.visitors.ast.classes import WrongMethodVisitor

method_template = """
class Test(object):
    def {0}(self, *args, **kwargs):
        {1}
"""

classmethod_template = """
class Test(object):
    @classmethod
    def {0}(cls, *args, **kwargs):
        {1}
"""


@pytest.mark.parametrize('code', [
    method_template,
    classmethod_template,
])
@pytest.mark.parametrize('method', [
    '__init__',
    '__new__',
    '__str__',
    '__aenter__',
    '__exit__',
    '__anext__',
    '__next__',
])
@pytest.mark.parametrize('statement', [
    'yield',
    'yield 1',
    'yield from some()',
])
def test_magic_generator(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
    code,
    method,
    statement,
):
    """Testing that magic method with `yield` is prohibited."""
    tree = parse_ast_tree(code.format(method, statement))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [YieldMagicMethodViolation])
    assert_error_text(visitor, method)


@pytest.mark.parametrize('code', [
    method_template,
    classmethod_template,
])
@pytest.mark.parametrize('method', [
    '__init__',
    '__new__',
    '__str__',
    '__aenter__',
    '__iter__',
    '__exit__',
    '__custom__',
])
@pytest.mark.parametrize('statement', [
    'return 1',
    'print()',
])
def test_magic_statement(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    method,
    statement,
):
    """Testing that magic method with statement is allowed."""
    tree = parse_ast_tree(code.format(method, statement))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    method_template,
    classmethod_template,
])
@pytest.mark.parametrize('method', [
    '__iter__',
    '__aiter__',
    '__call__',
    '__custom__',
])
@pytest.mark.parametrize('statement', [
    'yield',
    'yield 1',
    'yield from some()',
])
def test_iter_generator(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    method,
    statement,
):
    """Testing that some magic methods with `yield` are allowed."""
    tree = parse_ast_tree(code.format(method, statement))

    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
