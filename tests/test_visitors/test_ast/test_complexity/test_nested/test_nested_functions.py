import pytest

from wemake_python_styleguide.violations.best_practices import (
    NestedFunctionViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.nested import (
    NESTED_FUNCTIONS_WHITELIST,
    NestedComplexityVisitor,
)

# Functions:

nested_function_in_function = """
def container():
    def {0}(): ...
"""

nested_function_in_async_function = """
async def container():
    def {0}(): ...
"""

nested_async_function_in_async_function = """
async def container():
    async def {0}(): ...
"""

nested_async_function_in_function = """
def container():
    async def {0}(): ...
"""

nested_function_in_if = """
def container():
    if some_condition:
        def {0}(): ...
"""

nested_function_in_if_else = """
def container():
    if some_condition:
        ...
    else:
        def {0}(): ...
"""

nested_function_while_loop = """
def container():
    while True:
        def {0}(): ...
"""

nested_function_in_for_loop = """
def container():
    for some in iterable():
        def {0}(): ...
"""

nested_function_in_try = """
def container():
    try:
        def {0}(): ...
    except:
        ...
"""

nested_function_in_try_except = """
def container():
    try:
        ...
    except:
        def {0}(): ...
"""

nested_function_in_try_else = """
def container():
    try:
        ...
    except:
        ...
    else:
        def {0}(): ...
"""

nested_function_in_try_finally = """
def container():
    try:
        ...
    finally:
        def {0}(): ...
"""

# Methods:

nested_function_in_method = """
class Raw(object):
    def container(self):
        def {0}(): ...
"""

nested_function_in_async_method = """
class Raw(object):
    async def container(self):
        def {0}(): ...
"""

nested_async_function_in_async_method = """
class Raw(object):
    async def container(self):
        async def {0}(): ...
"""

nested_async_function_in_method = """
class Raw(object):
    def container(self):
        async def {0}(): ...
"""

# Lambdas:

lambda_in_function = """
def container():
    lazy_value = lambda: 12
"""

lambda_in_method = """
class Raw(object):
    def container(self):
        lazy_value = lambda: 12
"""

# Wrong lambdas:

lambda_in_lambda = 'inline = lambda: lambda value: value + 12'

lambda_in_lambda_in_function = """
def container():
    nested_lambda = lambda: lambda value: value + 12
"""

lambda_in_lambda_in_method = """
class Test(object):
    def container(self):
        return lambda: lambda value: value + 12
"""

lambda_in_call_in_lambda = """
def container():
    nested_lambda = lambda: map(lambda value: value + 12, [1, 2, 3])
"""


@pytest.mark.parametrize('nested_name', [
    'nested',
    '_nested',
    '__nested',
])
@pytest.mark.parametrize('code', [
    nested_function_in_function,
    nested_async_function_in_function,
    nested_function_in_async_function,
    nested_async_function_in_async_function,
    nested_function_in_method,
    nested_async_function_in_method,
    nested_function_in_async_method,
    nested_async_function_in_async_method,

    # Regression when functions were allowed to be nested in deep nodes:
    nested_function_in_if,
    nested_function_in_if_else,
    nested_function_while_loop,
    nested_function_in_for_loop,
    nested_function_in_try,
    nested_function_in_try_except,
    nested_function_in_try_else,
    nested_function_in_try_finally,
])
def test_nested_function(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    nested_name,
    default_options,
):
    """Testing that nested functions are restricted."""
    tree = parse_ast_tree(code.format(nested_name))

    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NestedFunctionViolation])
    assert_error_text(visitor, nested_name)


@pytest.mark.parametrize('whitelist_name', NESTED_FUNCTIONS_WHITELIST)
@pytest.mark.parametrize('code', [
    nested_function_in_function,
    nested_async_function_in_function,
    nested_function_in_async_function,
    nested_async_function_in_async_function,
    nested_function_in_method,
    nested_async_function_in_method,
    nested_function_in_async_method,
    nested_async_function_in_async_method,
])
def test_whitelist_nested_functions(
    assert_errors,
    parse_ast_tree,
    whitelist_name,
    code,
    default_options,
):
    """Testing that it is possible to nest whitelisted functions."""
    tree = parse_ast_tree(code.format(whitelist_name))

    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('whitelist_name', NESTED_FUNCTIONS_WHITELIST)
@pytest.mark.parametrize('code', [
    nested_function_in_if,
    nested_function_in_if_else,
    nested_function_while_loop,
    nested_function_in_for_loop,
    nested_function_in_try,
    nested_function_in_try_except,
    nested_function_in_try_else,
    nested_function_in_try_finally,
])
def test_deep_whitelist_nested_functions(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    whitelist_name,
    code,
    default_options,
    mode,
):
    """Testing that it is possible to nest whitelisted functions."""
    tree = parse_ast_tree(mode(code.format(whitelist_name)))

    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NestedFunctionViolation])
    assert_error_text(visitor, whitelist_name)


@pytest.mark.parametrize('code', [
    lambda_in_function,
    lambda_in_method,
])
def test_lambda_nested_functions(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that it is possible to nest lambda inside functions."""
    tree = parse_ast_tree(mode(code))

    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    lambda_in_lambda,
    lambda_in_lambda_in_function,
    lambda_in_lambda_in_method,
    lambda_in_call_in_lambda,
])
def test_lambda_nested_lambdas(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """
    Testing that it is restricted to nest lambdas.

    See: https://github.com/wemake-services/wemake-python-styleguide/issues/94
    """
    tree = parse_ast_tree(mode(code))

    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NestedFunctionViolation])
    assert_error_text(visitor, 'lambda')
