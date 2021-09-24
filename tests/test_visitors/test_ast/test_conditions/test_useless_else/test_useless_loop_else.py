import pytest

from wemake_python_styleguide.violations.refactoring import (
    UselessReturningElseViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import UselessElseVisitor

# Correct:

correct_example1 = """
def wrapper():
    for x in ...:
        raise ...
"""

correct_example2 = """
while ...:
    raise ...
"""

correct_example3 = """
def function():
    for x in ...:
        ...
    raise ...
"""

correct_example4 = """
while ...:
    ...
raise ...
"""

correct_example4 = """
def function():
    for x in ...:
        ...
    else:
        raise ...
"""

correct_example5 = """
def function():
    while ...:
        ...
    else:
        raise ...
"""

correct_example6 = """
def function():
    for x in ...:
        return
    else:
        ...
    return
"""

correct_example7 = """
def function():
    while ...:
        return
    else:
        ...
    return
"""

correct_example8 = """
def function():
    for x in ...:
        if ...:
            return 2
    return 1
"""

correct_example9 = """
def function():
    while ...:
        try:
            ...
        except ...:
           continue
        break
    else:
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
])
def test_else_that_can_not_be_removed(
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

while_loop = """
def wrapper():
    while ...:
        if ...:  # nested
            {0}
    else:
        {1}
"""

for_loop = """
def wrapper():
    for x in ...:
        ...
        {0}
        ...
    else:
        {1}
"""


@pytest.mark.parametrize('template', [
    while_loop,
    for_loop,
])
@pytest.mark.parametrize('code1', [
    'return',
    'raise ValueError()',
    'break',
    'continue',
])
@pytest.mark.parametrize('code2', [
    'return',
    'raise ValueError()',
])
def test_else_that_can_be_removed(
    assert_errors,
    parse_ast_tree,
    code1,
    code2,
    template,
    default_options,
    mode,
):
    """Testing that extra ``else`` blocks can be removed."""
    tree = parse_ast_tree(mode(template.format(code1, code2)))
    visitor = UselessElseVisitor(default_options, tree=tree)
    visitor.run()
    overrides = ['break']  # regression1958
    if code1 in overrides:
        # We might want to have an else statement
        # if the loop contains a break statement
        assert_errors(visitor, [])
    else:
        assert_errors(visitor, [UselessReturningElseViolation])


@pytest.mark.parametrize('template', [
    while_loop,
    for_loop,
])
@pytest.mark.parametrize('code', [
    'print()',
    'new_var = 1',
])
@pytest.mark.parametrize('returning', [
    'return',
    'raise ValueError()',
    'break',
    'continue',
])
def test_else_that_cannot_be_removed1(
    assert_errors,
    parse_ast_tree,
    code,
    returning,
    template,
    default_options,
    mode,
):
    """Testing that extra ``else`` blocks can be removed."""
    tree = parse_ast_tree(mode(template.format(returning, code)))

    visitor = UselessElseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    while_loop,
    for_loop,
])
@pytest.mark.parametrize('code', [
    'print()',
    'new_var = 1',
])
@pytest.mark.parametrize('returning', [
    'return',
    'raise ValueError()',
])
def test_else_that_cannot_be_removed2(
    assert_errors,
    parse_ast_tree,
    code,
    returning,
    template,
    default_options,
    mode,
):
    """Testing that extra ``else`` blocks can be removed."""
    tree = parse_ast_tree(mode(template.format(code, returning)))

    visitor = UselessElseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
