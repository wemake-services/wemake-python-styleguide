import pytest

from wemake_python_styleguide.violations.best_practices import (
    ControlVarUsedAfterBlockViolation,
)
from wemake_python_styleguide.visitors.ast.blocks import (
    AfterBlockVariablesVisitor,
)

# Correct:

correct_for_loop1 = """
def wrapper():
    for i, j in ():
        print(i, j)
"""

correct_for_loop2 = """
def wrapper():
    for i, j in ():
        return i, j
"""

correct_for_loop3 = """
def wrapper():
    for i, j in ():
        yield i, j
"""

correct_for_loop4 = """
def wrapper():
    for i, j in ():
        x = i + j
        print(x)
"""

correct_for_loop5 = """
def wrapper():
    for i in ():
        for j in ():
            print(i, j)
        print(i)
    print(wrapper)
"""

correct_for_multi_loops = """
def wrapper():
    for my_var in range(3):
        my_var = my_var + 3
    for my_var in range(4):
        my_var = my_var + 4
"""

correct_for_comprehension1 = """
def context():
    nodes = [
        print(compare.left)
        for compare in node.values
        if isinstance(compare, ast.Compare)
    ]
"""

correct_for_comprehension2 = """
def context():
    nodes = {
        compare.left: compare.right
        for compare in node.values
        if isinstance(compare, ast.Compare)
    }
"""

correct_for_comprehension3 = """
def context():
    nodes = (
        compare.left
        for compare in node.values
        if isinstance(compare, ast.Compare)
    )
"""

correct_for_comprehension4 = """
def context():
    nodes = {
        compare.left
        for compare in node.values
        if isinstance(compare, ast.Compare)
    }
"""

correct_except1 = """
try:
    ...
except Exception as e:
    print(e)
"""

correct_except2 = """
try:
    ...
except TypeError as type_error:
    print(type_error)
except Exception as e:
    print(e)
"""

correct_except3 = """
e = 1
try:
    ...
except Exception as e:
    ...
print(e)
"""

correct_except4 = """
try:
    ...
except Exception as e:
    ...
print(e)
"""

correct_except_regression1115 = """
try:
    vehicles = self.client.list_vehicles()
except tesla_api.AuthenticationError as e:
    self.client.close()
    raise GUIError(_("Login details are incorrect.")) from e
except tesla_api.aiohttp.client_exceptions.ClientConnectorError as e:
    self.client.close()
    raise GUIError(_("Network error")) from e
"""

correct_with1 = """
def wrapper():
    with open() as (first, second):
        print(first, second)
"""

correct_with2 = """
def wrapper():
    with open() as first:
        print(first)
    print(wrapper)
"""

correct_with3 = """
def wrapper():
    with open() as first:
        print(first)
    print(wrapper)

def other():
    first = 1
    print(first)
"""

# Wrong:

wrong_for_loop1 = """
def wrapper():
    for i, j in ():
        print(i, j)
    print(i)
"""

wrong_for_loop2 = """
def wrapper():
    for i, j in ():
        print(i, j)
    print(j)
"""

wrong_for_loop3 = """
def wrapper():
    for i in ():
        for j in ():
            print(i, j)
        print(i)
    print(j)
"""

wrong_with1 = """
def wrapper():
    with open() as first:
        ...
    print(first)
"""

wrong_with2 = """
def wrapper():
    with open() as (first, second):
        ...
    print(first)
"""

wrong_with3 = """
def wrapper():
    with open() as (first, second):
        ...
    print(second)
"""

wrong_block_variable_reuse1 = """
def wrapper():
    for my_var in range(3):
        my_var = my_var + 3
    with open() as my_var:
        my_var = my_var + 4
"""


@pytest.mark.parametrize('code', [
    wrong_for_loop1,
    wrong_for_loop2,
    wrong_for_loop3,
    wrong_with1,
    wrong_with2,
    wrong_with3,
    wrong_block_variable_reuse1,
])
def test_control_variable_used_after_block(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that using variable after the block is not allowed."""
    tree = parse_ast_tree(mode(code))

    visitor = AfterBlockVariablesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ControlVarUsedAfterBlockViolation])


@pytest.mark.parametrize('code', [
    correct_for_loop1,
    correct_for_loop2,
    correct_for_loop3,
    correct_for_loop4,
    correct_for_loop5,
    correct_for_multi_loops,
    correct_for_comprehension1,
    correct_for_comprehension2,
    correct_for_comprehension3,
    correct_for_comprehension4,
    correct_except1,
    correct_except2,
    correct_except3,
    correct_except4,
    correct_except_regression1115,
    correct_with1,
    correct_with2,
    correct_with3,
])
def test_control_variable_used_correctly(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that using variables inside a block is correct."""
    tree = parse_ast_tree(mode(code))

    visitor = AfterBlockVariablesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
