import pytest

from wemake_python_styleguide.violations.oop import (
    WrongDescriptorDecoratorViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    FunctionDefinitionVisitor,
)

# Correct:

correct_decorator1 = """
class Test(object):
    @classmethod
    def method(cls): ...
"""

correct_decorator2 = """
class Test(object):
    @first
    @second(param=4)
    @third()
    def method(cls): ...
"""

correct_decorator3 = """
class Test(object):
    @first
    @second(param=4)
    @classmethod
    def method(cls): ...
"""

correct_decorator4 = """
@first
@second(param=4)
@third()
def function(): ...
"""

# Wrong:

wrong_decorator1 = """
@classmethod
def function(): ...
"""

wrong_decorator2 = """
@staticmethod
def function(): ...
"""

wrong_decorator3 = """
@property
def function(): ...
"""

wrong_decorator4 = """
@classmethod
@staticmethod
@property
def function(): ...
"""


@pytest.mark.parametrize('code', [
    correct_decorator1,
    correct_decorator2,
    correct_decorator3,
    correct_decorator4,
])
def test_method_decorators_correct(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that too large amount of decorators works."""
    tree = parse_ast_tree(mode(code))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_decorator1,
    wrong_decorator2,
    wrong_decorator3,
    wrong_decorator4,
])
def test_method_decorators_incorrect(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that too large amount of decorators works."""
    tree = parse_ast_tree(mode(code))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongDescriptorDecoratorViolation])
