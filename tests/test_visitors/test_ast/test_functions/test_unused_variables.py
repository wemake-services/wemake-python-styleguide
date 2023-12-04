import pytest

from wemake_python_styleguide.violations.naming import (
    UnusedVariableIsUsedViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    FunctionDefinitionVisitor,
)

# Correct:

correct_module = """
_PROTECTED = 1
PUBLIC = _PROTECTED + 1
"""

correct_class = """
class Test(object):
    _constant = 1

    def __init__(self):
        self._protected = 1
        self.public = self._protected + 1

    def _protected_method(self):
        ...
"""

correct_function = """
def _some_function():
    first, _second, _ = some_tuple()
    print(first)
"""

correct_function_with_for = """
def some_function():
    for name, _phone in people.items():
        print(name)
"""

correct_function_with_exception = """
def some_function():
    try:
        ...
    except Exception as exc:
        print(exc)
"""

correct_function_with_unnamed_exception = """
def some_function():
    try:
        ...
    except Exception:
        ...
"""

correct_func_with_re_store_unused_variable1 = """
def logo_and_user():
    user, _ = some_tuple()
    logo, _ = some_tuple()
"""

correct_func_with_re_store_unused_variable2 = """
def logo_and_user():
    user, __ = some_tuple()
    logo, __ = some_tuple()
"""

# Wrong:

wrong_function1 = """
def some_function():
    _some = calling()
    print(_some)
"""

wrong_function2 = """
def some_function():
    first, _some = calling()
    print(_some)
"""

wrong_function_with_exception = """
def some_function():
    try:
        ...
    except Exception as _exc:
        print(_exc)
"""

wrong_function_with_with = """
def some_function():
    with some() as _ex:
        print(_ex)
"""

wrong_function_with_for = """
def some_function():
    for _key_item in some():
        print(_key_item)
"""

wrong_method = """
class Test(object):
    def some_method(self):
        _some = calling()
        print(_some)
"""

wrong_function_with_walrus = """
def some_function():
    if _unused := some():
        print(_unused)
"""


@pytest.mark.parametrize('code', [
    correct_module,
    correct_class,
    correct_function,
    correct_function_with_for,
    correct_function_with_exception,
    correct_function_with_unnamed_exception,
    correct_func_with_re_store_unused_variable1,
    correct_func_with_re_store_unused_variable2,
])
def test_correct_variables(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that correct usage of variables is allowed."""
    tree = parse_ast_tree(mode(code))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_function1,
    wrong_function2,
    wrong_function_with_exception,
    wrong_function_with_with,
    wrong_function_with_for,
    wrong_method,
    wrong_function_with_walrus,
])
def test_wrong_super_call(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that naming and using variables have limitations."""
    tree = parse_ast_tree(mode(code))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnusedVariableIsUsedViolation])


def test_double_wrong_variables(
    assert_errors,
    parse_ast_tree,
    default_options,
    mode,
):
    """Testing that it is possible to have two violations with wrong vars."""
    code = """
    def some_function():
        _should_not_be_used = 1
        print(_should_not_be_used)
        print(_should_not_be_used)
    """
    tree = parse_ast_tree(mode(code))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        UnusedVariableIsUsedViolation,
        UnusedVariableIsUsedViolation,
    ])
