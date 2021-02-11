import pytest

from wemake_python_styleguide.violations.refactoring import (
    UselessReturningElseViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import UselessElseVisitor

# Correct:

correct_example1 = """
def function():
    if some_condition:
        return None
    return None
"""

correct_example2 = """
def function():
    if some_condition:
        return None
"""

correct_example3 = """
def function():
    if some_condition:
        return None
    elif other_condition:
        return None
    return None
"""

correct_example4 = """
def function():
    if some_condition:
        ...
    else:
        return None
"""

correct_example4 = """
if some_condition:
    ...
else:
    raise ValueError()
"""

correct_example5 = """
if some_condition:
    if other:
        raise TypeError()
else:
    raise ValueError()
"""

correct_example6 = """
def function():
    if some_condition:
        if other:
            raise TypeError()
        elif other is None:
            ...
        else:
            ...
    else:
        raise ValueError()
"""

correct_example7 = """
def function():
    if some_condition:
        with open() as file:
            return file
    else:
        raise ValueError()
"""

correct_example8 = """
def function():
    if some_condition:
        ...
    elif other_condition:
        ...
    else:
        return None
"""

correct_example9 = """
def function():
    if some_condition:
        return None
    elif other_condition:
        return None
    else:
        print(1)
        print(2)
        if nested:
            return 1
"""

correct_example10 = """
def function():
    if some_condition:
        return None
    elif other_condition:
        return None
    raise ValueError()
"""

correct_example11 = """
def function():
    if some_condition:
        return None
    elif other_condition:
        ...
    else:
        raise ValueError()
"""

correct_example12 = """
def function():
    if some_condition:
        ...
    elif other_condition:
        return None
    else:
        raise ValueError()
"""

correct_example13 = """
def function():
    for test in some:
        if some_condition:
            continue
        elif other_condition:
            break
        raise ValueError()
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
    correct_example11,
    correct_example12,
    correct_example13,
])
def test_else_that_can_not_be_removed(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that extra ``else`` blocks cannot be removed."""
    tree = parse_ast_tree(mode(code))

    visitor = UselessElseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


# Wrong:

function_level_condition = """
def function():
    if some_condition:
        {0}
    else:
        {1}
"""

for_loop_level_condition = """
def wrapper():
    for _ in some_iterable:
        if some_condition:
            {0}
        else:
            {1}
"""

while_loop_level_condition = """
while True:
    if some_condition:
        {0}
    else:
        {1}
"""

module_level_condition = """
if some_condition:
    {0}
else:
    {1}
"""

multiple_ifs1 = """
def test():
    parent = get_parent(node)
    if parent is None:
        return None
    elif isinstance(parent, contexts):
        {0}
    else:
        {1}
"""

multiple_ifs2 = """
def test():
    parent = get_parent(node)
    if parent is None:
        {0}
    elif isinstance(parent, contexts):
        return None
    else:
        {1}
"""


@pytest.mark.parametrize('template', [
    function_level_condition,
    for_loop_level_condition,
    multiple_ifs1,
    multiple_ifs2,
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
    mode,
):
    """Testing that extra ``else`` blocks can be removed."""
    tree = parse_ast_tree(mode(template.format(code, code)))

    visitor = UselessElseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessReturningElseViolation])


@pytest.mark.parametrize('template', [
    multiple_ifs1,
    multiple_ifs2,
])
@pytest.mark.parametrize('code', [
    'return True',
    'return False',
])
def test_else_that_can_be_removed_and_complex_if(
    assert_errors,
    parse_ast_tree,
    code,
    template,
    default_options,
    mode,
):
    """Testing that extra ``else`` blocks can be removed."""
    tree = parse_ast_tree(mode(template.format(code, code)))

    visitor = UselessElseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessReturningElseViolation])


@pytest.mark.parametrize('template', [
    function_level_condition,
    for_loop_level_condition,
])
@pytest.mark.parametrize('code', [
    'return True',
    'return False',
])
def test_else_can_be_removed_and_simplifiable_if(
    assert_errors,
    parse_ast_tree,
    code,
    template,
    default_options,
    mode,
):
    """Extra ``else`` blocks can be removed, plus the ``if`` is simplifiable."""
    tree = parse_ast_tree(mode(template.format(code, code)))

    visitor = UselessElseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessReturningElseViolation])


@pytest.mark.parametrize('template', [
    for_loop_level_condition,
    while_loop_level_condition,
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
    mode,
):
    """Testing that extra ``else`` blocks can be removed."""
    tree = parse_ast_tree(mode(template.format(code, code)))

    visitor = UselessElseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessReturningElseViolation])


@pytest.mark.parametrize('template', [
    module_level_condition,
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
    function_level_condition,
    for_loop_level_condition,
    while_loop_level_condition,
    module_level_condition,
    multiple_ifs1,
    multiple_ifs2,
])
@pytest.mark.parametrize('code', [
    'print()',
    'new_var = 1',
])
def test_else_that_can_not_be_removed(
    assert_errors,
    parse_ast_tree,
    template,
    code,
    default_options,
    mode,
):
    """Testing that extra ``else`` blocks cannot be removed."""
    tree = parse_ast_tree(mode(template.format(code, 'raise ValueError()')))

    visitor = UselessElseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
