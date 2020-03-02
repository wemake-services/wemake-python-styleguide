import pytest

from wemake_python_styleguide.violations.refactoring import (
    TypeCompareViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    WrongFunctionCallContextVisitior,
)

# Wrong:

simple_compare = '{0} == other'
is_compare = '{0} is other'
nested_compare = '{0} == int and other()'
triple_compare = '{0} == some == other'

if_case = """
if {0} == int:
    ...
"""

# Correct:

expression = '{0}'
assignment = 'some = {0}'
annotation = 'some: {0} = int'

try_finally = """
try:
    file = {0}
finally:
    ...
"""

function_return = """
def function():
    return {0}
"""


@pytest.mark.parametrize('code', [
    expression,
    assignment,
    annotation,
    try_finally,
    function_return,
])
@pytest.mark.parametrize('call', [
    'type()',
    'type(some)',
    'type("TypeName", (object,), dict())',
])
def test_type_regular_usage(
    assert_errors,
    parse_ast_tree,
    code,
    call,
    default_options,
    mode,
):
    """Testing that ``type()`` can be used."""
    tree = parse_ast_tree(mode(code.format(call)))

    visitor = WrongFunctionCallContextVisitior(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    simple_compare,
    is_compare,
    nested_compare,
    triple_compare,

    expression,
    assignment,
    annotation,
    try_finally,
    function_return,
])
@pytest.mark.parametrize('call', [
    'close()',
    'type.attr',
    'type.attr()',
    'obj.type()',
    'Type[T]',
])
def test_not_type_functions(
    assert_errors,
    parse_ast_tree,
    code,
    call,
    default_options,
    mode,
):
    """Testing that regular calls work."""
    tree = parse_ast_tree(mode(code.format(call)))

    visitor = WrongFunctionCallContextVisitior(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    simple_compare,
    is_compare,
    nested_compare,
    triple_compare,
])
@pytest.mark.parametrize('call', [
    'type()',
    'type(some)',
    'type("TypeName", (object,), dict())',
])
def test_type_with_compare(
    assert_errors,
    parse_ast_tree,
    code,
    call,
    default_options,
    mode,
):
    """Testing that ``type()`` cannot be used inside a compare."""
    tree = parse_ast_tree(mode(code.format(call)))

    visitor = WrongFunctionCallContextVisitior(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TypeCompareViolation])
