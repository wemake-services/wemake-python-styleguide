# -*- coding: utf-8 -*-

import string

import pytest

from wemake_python_styleguide.violations.naming import (
    AnonymousVariableUseViolation,
)
from wemake_python_styleguide.visitors.ast.naming import (
    VARIABLE_NAMES_BLACKLIST,
    WrongNameVisitor,
    WrongVariableUseVisitor,
)

import_name = 'import {0}'
from_import_module = 'from {0} import some'
from_import_name = 'from some import {0}'

calling_function = 'print({0})'
called_function = '{0}()'
calling_method = 'instance.call({0})'
called_method = 'instance.{0}()'
accessing_attribute = 'instance.{0}'
accessed_attribute = '{0}.attribute'
raising_variable = 'raise {0}'

returning_variable = """
def function():
    return {0}
"""

awaiting_variable = """
async def function():
    await {0}
"""

yielding_variable = """
def function():
    yield {0}
"""

anonymous_variable_store_one = """
_ = 4 + 5
"""

anonymous_variable_store_two = """
_, var = 'foo', 'bar'
"""

anonymous_variable_store_load_one = """
_ = 4 + 5
print(_)
"""

anonymous_variable_store_load_two = """
[_ for _ in range(5)]
"""


@pytest.mark.parametrize('bad_name', [
    *VARIABLE_NAMES_BLACKLIST,
    *string.ascii_letters,
    '__Class_private',
    'number_prefix_10',
    'some__underscores',
    'camelCase',
    'UPPER_case',
])
@pytest.mark.parametrize('code', [
    import_name,
    from_import_module,
    from_import_name,
    calling_function,
    called_function,
    calling_method,
    called_method,
    accessing_attribute,
    accessed_attribute,
    raising_variable,
    returning_variable,
    awaiting_variable,
    yielding_variable,
])
def test_wrong_variable_names(
    assert_errors,
    parse_ast_tree,
    bad_name,
    code,
    default_options,
):
    """Testing that any variable can used without raising violations."""
    tree = parse_ast_tree(code.format(bad_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    anonymous_variable_store_one,
    anonymous_variable_store_two,
])
def test_anonymous_variable_use_correct(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Ensures that anonymous variables are used to discard values."""
    tree = parse_ast_tree(code)

    visitor = WrongVariableUseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    anonymous_variable_store_load_one,
    anonymous_variable_store_load_two,
])
def test_anonymous_variable_use_wrong(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Ensures that anonymous variables are not used to store values."""
    tree = parse_ast_tree(code)

    visitor = WrongVariableUseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [AnonymousVariableUseViolation])
