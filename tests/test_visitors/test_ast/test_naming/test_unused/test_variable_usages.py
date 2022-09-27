import pytest

from wemake_python_styleguide.compat.constants import PY310
from wemake_python_styleguide.violations.naming import (
    UnusedVariableIsUsedViolation,
)
from wemake_python_styleguide.visitors.ast.naming.validation import (
    WrongNameVisitor,
)
from wemake_python_styleguide.visitors.ast.naming.variables import (
    UnusedVariableUsageVisitor,
)

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

pattern_match_usage = """
match {0}:
    case []: ...
"""


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
    '_',  # this is a different visitor
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
    pytest.param(
        pattern_match_usage,
        marks=pytest.mark.skipif(not PY310, reason='pm was added in 3.10'),
    ),
])
@pytest.mark.parametrize('visitor_class', [
    # We test it here,
    # since I am too lazy to refactor usage patterns to be a fixture.
    WrongNameVisitor,

    # Our real visitor.
    UnusedVariableUsageVisitor,
])
def test_correct_variable_usage(
    assert_errors,
    parse_ast_tree,
    bad_name,
    code,
    default_options,
    visitor_class,
):
    """Testing that any variable can used without raising violations."""
    tree = parse_ast_tree(code.format(bad_name))

    visitor = visitor_class(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('bad_name', [
    '__',
    '___',
])
@pytest.mark.parametrize('code', [
    annotation,
    annotation_value,
    assigned,
    assigned_attribute,
    calling_function,
    calling_star_function,
    called_function,
    calling_method,
    accessed_attribute,
    key_access,
    list_definition,
    raising_variable,
    returning_variable,
    awaiting_variable,
    yielding_variable,
    inheriting_variables,
])
def test_wrong_variable_usage(
    assert_errors,
    parse_ast_tree,
    bad_name,
    code,
    default_options,
):
    """Testing that any variable cannot be used if it is marked as unused."""
    tree = parse_ast_tree(code.format(bad_name))

    visitor = UnusedVariableUsageVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnusedVariableIsUsedViolation])


@pytest.mark.parametrize('bad_name', [
    '_',  # we are forced to allow this name, because django uses it a lot.
])
@pytest.mark.parametrize('code', [
    annotation,
    annotation_value,
    assigned,
    assigned_attribute,
    calling_function,
    calling_star_function,
    called_function,
    calling_method,
    accessed_attribute,
    key_access,
    list_definition,
    raising_variable,
    returning_variable,
    awaiting_variable,
    yielding_variable,
    inheriting_variables,
])
def test_unused_special_case(
    assert_errors,
    parse_ast_tree,
    bad_name,
    code,
    default_options,
):
    """Testing that any variable cannot be used if it is marked as unused."""
    tree = parse_ast_tree(code.format(bad_name))

    visitor = UnusedVariableUsageVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
