import pytest

from wemake_python_styleguide.violations.refactoring import (
    UselessReturningElseViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import UselessElseVisitor

# Correct:

correct_example1 = """
def function():
    try:
        ...
    except ...:
        return None
    return None
"""

correct_example2 = """
def function():
    try:
        ...
    except ...:
        ...
    return None
"""

correct_example3 = """
def function():
    try:
        ...
    except ...:
        return None
    except:
        ...
    return None
"""

correct_example4 = """
def function():
    try:
        ...
    except ...:
        return None
    else:
        ...
"""

correct_example4 = """
def function():
    try:
        ...
    except ...:
        ...
    else:
        return None
"""

correct_example5 = """
def function():
    try:
        ...
    except ...:
        ...
    else:
        return None
    return other
"""

correct_example6 = """
def function():
    try:
        ...
    except ...:
        return None
    else:
        return None
    finally:
        ...
"""

correct_example7 = """
def function():
    try:
        ...
    except ...:
        return None
    else:
        ...
    finally:
        ...
    return None
"""

correct_example8 = """
def function():
    try:
        ...
    finally:
        ...
    return None
"""

correct_example9 = """
try:
    ...
except ...:
    raise ...
else:
    ...
raise ...
"""

correct_example10 = """
try:
    ...
except ...:
    raise ...
raise ...
"""


@pytest.mark.parametrize('code', [
    correct_example1,
    correct_example2,
    correct_example3,
    correct_example4,
    correct_example5,
    correct_example6,
    correct_example7,
    correct_example8,
    correct_example9,
    correct_example10,
])
def test_else_that_can_not_be_removed1(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that extra ``else`` blocks cannot be removed."""
    tree = parse_ast_tree(code)

    visitor = UselessElseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


# Templates:

try_except_else = """
def function():
    try:
        ...
    except:
        {0}
    else:
        {1}
"""

try_multiple_except_else = """
def function():
    try:
        ...
    except ...:
        {0}
    except ...:
        {0}
    except:
        {0}
    else:
        {1}
"""

try_except_else_loop = """
while ...:
    try:
        ...
    except:
        {0}
    else:
        {1}
"""

try_except_else_module = """
try:
    ...
except:
    {0}
else:
    {1}
"""


@pytest.mark.parametrize('template', [
    try_except_else,
    try_multiple_except_else,
])
@pytest.mark.parametrize('code', [
    'return',
    'raise ValueError()',
])
def test_else_that_can_be_removed_in_function(
    assert_errors,
    parse_ast_tree,
    code,
    template,
    default_options,
):
    """Testing that extra ``else`` blocks can be removed."""
    tree = parse_ast_tree(template.format(code, code))

    visitor = UselessElseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessReturningElseViolation])


@pytest.mark.parametrize('template', [
    try_except_else_loop,
])
@pytest.mark.parametrize('code', [
    'break',
    'raise ValueError()',
    'continue',
])
def test_else_that_can_be_removed_in_loop(
    assert_errors,
    parse_ast_tree,
    template,
    code,
    default_options,
):
    """Testing that extra ``else`` blocks can be removed."""
    tree = parse_ast_tree(template.format(code, code))

    visitor = UselessElseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessReturningElseViolation])


@pytest.mark.parametrize('template', [
    try_except_else_module,
])
@pytest.mark.parametrize('code', [
    'raise ValueError()',
])
def test_else_that_can_be_removed_in_module(
    assert_errors,
    parse_ast_tree,
    template,
    code,
    default_options,
):
    """Testing that extra ``else`` blocks can be removed."""
    tree = parse_ast_tree(template.format(code, code))

    visitor = UselessElseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessReturningElseViolation])


@pytest.mark.parametrize('template', [
    try_except_else,
    try_multiple_except_else,
    try_except_else_loop,
    try_except_else_module,
])
@pytest.mark.parametrize('code', [
    'print()',
    'new_var = 1',
])
@pytest.mark.parametrize('returning', [
    'raise ValueError()',
])
def test_else_that_can_not_be_removed2(
    assert_errors,
    parse_ast_tree,
    template,
    code,
    returning,
    default_options,
):
    """Testing that extra ``else`` blocks cannot be removed."""
    tree = parse_ast_tree(template.format(code, returning))

    visitor = UselessElseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
