# -*- coding: utf-8 -*-

import string

import pytest

from wemake_python_styleguide.visitors.ast.naming import (
    VARIABLE_NAMES_BLACKLIST,
    WrongNameVisitor,
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


@pytest.mark.parametrize('bad_name', [
    *VARIABLE_NAMES_BLACKLIST,
    *string.ascii_letters,
    '__Class_private',
    'number_prefix_10',
    'some__underscores',
    'camelCase',
    'UPPER_case',
    'юникод',
    'wrong_alias_',
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
