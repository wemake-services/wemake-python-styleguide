import pytest

from wemake_python_styleguide.violations.best_practices import (
    MixingFunctionArgumentTypesViolation,
)

from wemake_python_styleguide.visitors.ast.functions import (
    FunctionSignatureVisitor,
)

# Correct:
correct_function1 = """
def first(first: int = 0, second: int = 1) :
    ...
"""
correct_function2 = """
def first(*args) :
    ...
"""

correct_function3 = """
def first(first: int = 0, **kwargs) :
    ...
"""

correct_function4 = """
def first(first: int, *, second: int) :
    ...
"""

correct_function5 = """
def first(first: int, *, second: int = 0) :
    ...
"""

# Wrong:
wrong_function1 = """
def first(first: int = 0, *args) :
    ...
"""

wrong_function2 = """
def second(first: int = 0, second: int = 0, *args) :
    ...
"""

wrong_function3 = """
def first(first: int = 0, *, second: int): 
    ...
"""

wrong_function4 = """
def second(first: int = 0, *, second: int = 0): 
    ...
"""


@pytest.mark.parametrize('code', [
    correct_function1,
    correct_function2,
    correct_function3,
    correct_function4,
    correct_function5,
])
def test_not_mixed_arguments(
    assert_errors,
    parse_ast_tree,
    code,
    mode,
    default_options,
):
    """Testing that regular functions are allowed."""
    tree= parse_ast_tree(mode(code))

    visitor = FunctionSignatureVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_function1,
    wrong_function2,
    wrong_function3,
    wrong_function4,
])
def test_mixed_arguments(
    assert_errors,
    parse_ast_tree,
    code,
    mode,
    default_options,
):
    """Testing that functions with positional parameters with default values and 
    keyword-only paramters aren't allowed. Also tests that functions with 
    positional arguments with default values amd *args aren't allowed."""
    tree = parse_ast_tree(mode(code))

    visitor = FunctionSignatureVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MixingFunctionArgumentTypesViolation])
