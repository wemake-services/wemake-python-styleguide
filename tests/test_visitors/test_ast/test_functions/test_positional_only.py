import pytest

from wemake_python_styleguide.violations.best_practices import (
    PositionalOnlyArgumentsViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    FunctionSignatureVisitor,
)

# Correct:
correct_lambda = 'lambda x, *args, y, z = 1, **kwargs: ...'
correct_function = """
def function(first, *args, second, third: int = 1, **kwargs) -> None:
    ...
"""

correct_method = """
class Test(object):
    def function(self, first, *args, second, z: int = 1, **kwargs) -> None:
        ...
"""

# Wrong:
wrong_lambda1 = 'lambda a, /, b: ...'
wrong_lambda2 = 'lambda a, /, x, *args, y, z = 1, **kwargs: ...'
wrong_function1 = """
def function(a, /) -> None:
    ...
"""

wrong_function2 = """
def function(a: int, /, b):
    ...
"""

wrong_function3 = """
def function(a, /, first, *args, second, third: int = 1, **kwargs) -> None:
    ...
"""

wrong_method1 = """
class Test(object):
    def function(self, /, first):
        ...
"""

wrong_method2 = """
class Test(object):
    def function(self, /, first, *args, second, z: int = 1, **kwargs) -> None:
        ...
"""


@pytest.mark.parametrize('code', [
    correct_lambda,
    correct_function,
    correct_method,
])
def test_not_posonlyargs(
    assert_errors,
    parse_ast_tree,
    code,
    mode,
    default_options,
):
    """Testing that regular code is allowed."""
    tree = parse_ast_tree(mode(code))

    visitor = FunctionSignatureVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_lambda1,
    wrong_lambda2,
    wrong_function1,
    wrong_function2,
    wrong_function3,
    wrong_method1,
    wrong_method2,
])
def test_posonyargs(
    assert_errors,
    parse_ast_tree,
    code,
    mode,
    default_options,
):
    """Testing that ``/`` is not allowed."""
    tree = parse_ast_tree(mode(code))

    visitor = FunctionSignatureVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [PositionalOnlyArgumentsViolation])
