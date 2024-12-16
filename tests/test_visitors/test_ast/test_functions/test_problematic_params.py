import pytest

from wemake_python_styleguide.violations.best_practices import (
    ProblematicFunctionParamsViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    FunctionSignatureVisitor,
)

# Wrong:

problematic_function1 = """
def function(arg1, arg2=2, arg3=3, /):
    ...
"""

problematic_function2 = """
def function(arg1, arg2=2, arg3=3, arg4=4, /):
    ...
"""

problematic_function3 = """
def function(arg1, arg2=2, arg3=3, arg4=4, /, arg5=5):
    ...
"""

problematic_function4 = """
def function(arg1=1, /, *args):
    ...
"""

problematic_function5 = """
def function(arg1=1, *args):
    ...
"""

problematic_function6 = 'lambda x=1, y=2, /: ...'

# Correct:

correct_function1 = """
def function(arg1, *args):
    ...
"""

correct_function2 = """
def function(arg1, /, *args):
    ...
"""

correct_function3 = """
def function(arg1=1, /):
    ...
"""

correct_function4 = """
def function(arg1, arg2=2, /):
    ...
"""

correct_function5 = 'lambda arg1, arg2=2, /: ...'


@pytest.mark.parametrize(
    'code',
    [
        problematic_function1,
        problematic_function2,
        problematic_function3,
        problematic_function4,
        problematic_function5,
        problematic_function6,
    ],
)
def test_wrong_function_params(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that wrong function params are forbidden."""
    tree = parse_ast_tree(mode(code))

    visitor = FunctionSignatureVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ProblematicFunctionParamsViolation])


@pytest.mark.parametrize(
    'code',
    [
        correct_function1,
        correct_function2,
        correct_function3,
        correct_function4,
        correct_function5,
    ],
)
def test_correct_function_params(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that wrong function params are forbidden."""
    tree = parse_ast_tree(mode(code))

    visitor = FunctionSignatureVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
