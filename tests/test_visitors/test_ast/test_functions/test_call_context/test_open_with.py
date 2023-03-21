import pytest

from wemake_python_styleguide.violations.refactoring import (
    OpenWithoutContextManagerViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    WrongFunctionCallContextVisitor,
)

# Correct:

context_manager1 = """
def wrapper():
    with {0} as file:
        ...
"""

context_manager2 = """
def wrapper():
    with {0}:
        ...
"""

context_manager3 = """
def wrapper():
    with first, {0} as some:
        ...
"""

context_manager4 = """
def wrapper():
    with {0} as some, second:
        ...
"""

context_manager5 = """
def wrapper():
    with ({0} if check else nullcontext()) as x:
        ...
"""


# Wrong:

expression = '{0}'
assignment = 'some = {0}'

try_finally = """
try:
    file = {0}
finally:
    ...
"""


@pytest.mark.parametrize('code', [
    context_manager1,
    context_manager2,
    context_manager3,
    context_manager4,
    context_manager5,
])
@pytest.mark.parametrize('call', [
    'open()',
    'open("filename")',
    'open("filename", mode="rb")',
])
def test_open_inside_context_manager(
    assert_errors,
    parse_ast_tree,
    code,
    call,
    default_options,
    mode,
):
    """Testing that ``open()`` inside a context manager works."""
    tree = parse_ast_tree(mode(code.format(call)))

    visitor = WrongFunctionCallContextVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    context_manager1,
    context_manager2,
    context_manager3,
    context_manager4,
    expression,
    assignment,
    try_finally,
])
@pytest.mark.parametrize('call', [
    'close()',
    'open.attr',
    'open.attr()',
    'obj.open()',
])
def test_regular_functions(
    assert_errors,
    parse_ast_tree,
    code,
    call,
    default_options,
    mode,
):
    """Testing that regular calls work."""
    tree = parse_ast_tree(mode(code.format(call)))

    visitor = WrongFunctionCallContextVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    expression,
    assignment,
    try_finally,
])
@pytest.mark.parametrize('call', [
    'open()',
    'open("filename")',
    'open("filename", mode="rb")',
])
def test_open_without_context_manager(
    assert_errors,
    parse_ast_tree,
    code,
    call,
    default_options,
    mode,
):
    """Testing that ``open()`` without context managers raise a violation."""
    tree = parse_ast_tree(mode(code.format(call)))

    visitor = WrongFunctionCallContextVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [OpenWithoutContextManagerViolation])
