import pytest

from wemake_python_styleguide.violations.best_practices import (
    GetterWithoutReturnViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    FunctionSignatureVisitor,
)

getter_function_with_implicit_return = """
def get_foo():
    print('Hello world!')
"""

getter_function_with_bare_return = """
def get_foo():
    return
"""

getter_function_with_valued_return = """
def get_foo():
    return 1
"""

getter_function_with_explicit_none_return = """
def get_foo():
    return None
"""

getter_function_with_bare_yield = """
def get_foo():
    yield
"""

getter_function_with_valued_yield = """
def get_foo():
    yield 1
"""

getter_function_with_explicit_none_yield = """
def get_foo():
    yield None
"""

getter_function_with_yield_from = """
def get_foo():
    yield from [1]
"""

getter_method_with_implicit_return = """
class Foo:
    def get_foo(self):
        print('Hello world')
"""

getter_method_with_bare_return = """
class Foo:
    def get_foo(self):
        return
"""

getter_method_with_valued_return = """
class Foo:
    def get_foo(self):
        return 1
"""

getter_method_with_explicit_none_return = """
class Foo:
    def get_foo(self):
        return None
"""

getter_method_with_bare_yield = """
class Foo:
    def get_foo(self):
        yield
"""

getter_method_with_valued_yield = """
class Foo:
    def get_foo(self):
        yield 1
"""

getter_method_with_explicit_none_yield = """
class Foo:
    def get_foo(self):
        yield None
"""

getter_method_with_yield_from = """
class Foo:
    def get_foo(self):
        yield from [1]
"""

regular_function_with_bare_return = """
class Foo:
    def foo(self):
        return
"""

regular_function_with_implicit_return = """
class Foo:
    def foo(self):
        print('Hello World!')
"""

regular_function_with_bare_return = """
class Foo:
    def foo(self):
        return
"""

regular_function_with_bare_yield = """
class Foo:
    def foo(self):
        yield
"""

regular_method_with_bare_return = """
class Foo:
    def foo(self):
        return
"""

regular_method_with_implicit_return = """
class Foo:
    def foo(self):
        print('Hello world')
"""

regular_method_with_bare_return = """
class Foo:
    def foo(self):
        return
"""

regular_method_with_bare_yield = """
class Foo:
    def foo(self):
        yield
"""

getter_method_with_branched_return = """
def get_foo():
    if bar:
        return 1
"""

getter_stub_with_docstring = """
def get_foo():
    '''Gets foo.'''
"""

getter_stub_with_ellipsis = """
def get_foo():
    ...
"""

getter_stub_with_raise = """
def get_foo():
    raise ValueError('Error')
"""

getter_stub_with_docstring_and_ellipsis = """
def get_foo():
    '''Gets foo.'''
    ...
"""

getter_stub_with_docstring_and_raise = """
def get_foo():
    '''Gets Foo.'''
    raise ValueError('Error')
"""

getter_stub_with_extra_statements = """
def get_foo():
    '''Gets foo.'''
    print('Hello World')
    ...
"""


@pytest.mark.parametrize('code', [
    getter_function_with_implicit_return,
    getter_function_with_bare_return,
    getter_method_with_implicit_return,
    getter_method_with_bare_return,
    getter_stub_with_extra_statements,
])
def test_wrong_getters(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that getters which do not output values are forbidden."""
    tree = parse_ast_tree(mode(code))

    visitor = FunctionSignatureVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [GetterWithoutReturnViolation])


@pytest.mark.parametrize('code', [
    getter_function_with_valued_return,
    getter_function_with_explicit_none_return,
    getter_function_with_bare_yield,
    getter_function_with_valued_yield,
    getter_function_with_explicit_none_yield,
    getter_method_with_valued_return,
    getter_method_with_explicit_none_return,
    getter_method_with_bare_yield,
    getter_method_with_valued_yield,
    getter_method_with_explicit_none_yield,
    getter_method_with_branched_return,
    getter_stub_with_docstring,
    getter_stub_with_ellipsis,
    getter_stub_with_raise,
    getter_stub_with_docstring_and_ellipsis,
    getter_stub_with_docstring_and_raise,
])
def test_correct_getters(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that getters which output values are allowed."""
    tree = parse_ast_tree(mode(code))

    visitor = FunctionSignatureVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    getter_function_with_yield_from,
    getter_method_with_yield_from,
])
def test_correct_getter_with_yield_from(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """
    Testing that getters with ``yield from`` expressions are allowed.

    They need to be tested separately because ``yield from`` cannot be
    used in ``async`` functions.
    """
    tree = parse_ast_tree(code)

    visitor = FunctionSignatureVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    regular_function_with_bare_return,
    regular_function_with_implicit_return,
    regular_function_with_bare_yield,
    regular_method_with_bare_return,
    regular_method_with_implicit_return,
    regular_method_with_bare_yield,
])
def test_correct_non_getters(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that non-getter functions are allowed to not output values."""
    tree = parse_ast_tree(mode(code))

    visitor = FunctionSignatureVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
