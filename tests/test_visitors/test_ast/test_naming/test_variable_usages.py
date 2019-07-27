# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.naming import WrongNameVisitor

annotation = 'some_var: {0}'
annotation_value = 'some_var: {0} = None'
assigned = 'some_var = {0}'
assigned_attribute = '{0}.attribute = 1'

import_name = 'import {0}'
from_import_module = 'from {0} import some'
from_import_name = 'from some import {0}'

calling_function = 'print({0})'
calling_star_function = 'print(*{0})'
called_function = '{0}()'
calling_method = 'instance.call({0})'
called_method = 'instance.{0}()'
accessing_attribute = 'instance.{0}'
accessed_attribute = '{0}.attribute'

key_access = 'instance[{0}]'
list_definition = 'instance = [{0}, 1]'

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

inheriting_variables = 'class ValidName({0}): ...'


@pytest.mark.parametrize('bad_name', [
    'value',  # blacklisted
    'x',  # short
    '__Class_private',
    'number_prefix_10',
    'some__underscores',
    'camelCase',
    'UPPER_case',
    'юникод',
    'wrong_alias_',
])
@pytest.mark.parametrize('code', [
    annotation,
    annotation_value,
    assigned,
    assigned_attribute,
    import_name,
    from_import_module,
    from_import_name,
    calling_function,
    calling_star_function,
    called_function,
    calling_method,
    called_method,
    accessing_attribute,
    accessed_attribute,
    key_access,
    list_definition,
    raising_variable,
    returning_variable,
    awaiting_variable,
    yielding_variable,
    inheriting_variables,
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
