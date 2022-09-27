from textwrap import indent

import pytest

from wemake_python_styleguide.violations.naming import (
    UnusedVariableIsDefinedViolation,
)
from wemake_python_styleguide.visitors.ast.naming.variables import (
    UnusedVariableDefinitionVisitor,
)

module_context = '{0}'

function_context = """
def function():
{0}
"""

method_context = """
class Test(object):
    def function():
    {0}
"""


@pytest.mark.parametrize(('context', 'indentation'), [
    (function_context, 4),
    (method_context, 8),
])
@pytest.mark.parametrize('bad_name', [
    '(_first, _second)',
])
def test_unused_variable_tuple_definition(
    assert_errors,
    parse_ast_tree,
    context,
    indentation,
    bad_name,
    forbidden_tuple_unused_template,
    default_options,
    mode,
):
    """Testing tuples with all unused variables cannot be defined."""
    tree = parse_ast_tree(
        mode(context.format(
            indent(
                forbidden_tuple_unused_template.format(bad_name),
                ' ' * indentation,
            ),
        )),
    )

    visitor = UnusedVariableDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnusedVariableIsDefinedViolation])


@pytest.mark.parametrize(('context', 'indentation'), [
    (module_context, 0),
    (function_context, 4),
    (method_context, 8),
])
@pytest.mark.parametrize('bad_name', [
    '(first, second)',
    '(first, _second)',
    '(_first, second)',
])
def test_used_variable_tuple_definition_allowed(
    assert_errors,
    parse_ast_tree,
    context,
    indentation,
    bad_name,
    forbidden_tuple_unused_template,
    default_options,
    mode,
):
    """Testing tuples with at least one used variable can be defined."""
    tree = parse_ast_tree(
        mode(context.format(
            indent(
                forbidden_tuple_unused_template.format(bad_name),
                ' ' * indentation,
            ),
        )),
    )

    visitor = UnusedVariableDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(('context', 'indentation'), [
    (module_context, 0),
    (function_context, 4),
    (method_context, 8),
])
@pytest.mark.parametrize('bad_name', [
    '_',
    '__',
])
def test_raw_unused_variable_definition(
    assert_errors,
    parse_ast_tree,
    context,
    indentation,
    bad_name,
    forbidden_raw_unused_template,
    skip_match_case_syntax_error,
    default_options,
    mode,
):
    """Testing raw variable definition is forbidden in some cases."""
    skip_match_case_syntax_error(forbidden_raw_unused_template, bad_name)
    tree = parse_ast_tree(
        mode(context.format(
            indent(
                forbidden_raw_unused_template.format(bad_name),
                ' ' * indentation,
            ),
        )),
    )

    visitor = UnusedVariableDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnusedVariableIsDefinedViolation])


@pytest.mark.parametrize(('context', 'indentation'), [
    (module_context, 0),
    (function_context, 4),
    (method_context, 8),
])
@pytest.mark.parametrize('bad_name', [
    '_',
    '__',
])
def test_raw_unused_variable_definition_allowed(
    assert_errors,
    parse_ast_tree,
    context,
    indentation,
    bad_name,
    allowed_raw_unused_template,
    default_options,
    mode,
):
    """Testing raw variable definition is allowed in some cases."""
    tree = parse_ast_tree(
        mode(context.format(
            indent(
                allowed_raw_unused_template.format(bad_name),
                ' ' * indentation,
            ),
        )),
    )

    visitor = UnusedVariableDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(('context', 'indentation'), [
    (function_context, 4),
    (method_context, 8),
])
@pytest.mark.parametrize('bad_name', [
    '_protected',
])
def test_protected_unused_variable_definition(
    assert_errors,
    parse_ast_tree,
    context,
    indentation,
    bad_name,
    forbidden_protected_unused_template,
    default_options,
    mode,
):
    """Testing protected variable definition is forbidden in certain cases."""
    tree = parse_ast_tree(
        mode(context.format(
            indent(
                forbidden_protected_unused_template.format(bad_name),
                ' ' * indentation,
            ),
        )),
    )

    visitor = UnusedVariableDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnusedVariableIsDefinedViolation])


@pytest.mark.parametrize(('context', 'indentation'), [
    (module_context, 0),
    (function_context, 4),
    (method_context, 8),
])
@pytest.mark.parametrize('bad_name', [
    '_protected',
])
def test_protected_unused_var_definition_allowed(
    assert_errors,
    parse_ast_tree,
    context,
    indentation,
    bad_name,
    allowed_protected_unused_template,
    default_options,
    mode,
):
    """Testing protected variable definition is allowed in certain cases."""
    tree = parse_ast_tree(
        mode(context.format(
            indent(
                allowed_protected_unused_template.format(bad_name),
                ' ' * indentation,
            ),
        )),
    )

    visitor = UnusedVariableDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(('context', 'indentation'), [
    (module_context, 0),
    (function_context, 4),
    (method_context, 8),
])
@pytest.mark.parametrize('bad_name', [
    'regular',
    'list_',
])
def test_used_variable_definition_allowed(
    assert_errors,
    parse_ast_tree,
    context,
    indentation,
    bad_name,
    naming_template,
    default_options,
    mode,
):
    """Testing that any variable can be used if it is marked as used."""
    tree = parse_ast_tree(
        mode(context.format(
            indent(
                naming_template.format(bad_name), ' ' * indentation,
            ),
        )),
    )

    visitor = UnusedVariableDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
