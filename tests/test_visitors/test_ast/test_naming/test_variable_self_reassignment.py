import pytest

from wemake_python_styleguide.violations.best_practices import (
    ReassigningVariableToItselfViolation,
)
from wemake_python_styleguide.visitors.ast.naming.variables import (
    WrongVariableAssignmentVisitor,
)

# Correct:

right_fragment = """
test_variable = 5
test_variable = 10
"""

right_typed_fragment = """
test_variable: int = 5
test_variable: int = 10
"""

right_just_types = """
first_type: int
second_type: first_type
"""

right_fragment_tuple_assignment = """
x = 1
y = 2
x, y = y, x
"""

right_fragment_triple_tuple_assignment = """
x = 1
y = 2
z = 3
x, y, z = z, x, y
"""

right_star_assignment1 = """
x = 1
y = 2
y, *x = x, y
"""

right_star_assignment2 = """
x = 1
y = 2
x, *y = y, x
"""

right_star_assignment3 = """
x = 1
y = 2
z = 3
x, *y = z, x, y
"""

# regression 1812
# https://github.com/wemake-services/wemake-python-styleguide/issues/1812
right_parts_unused1 = 'x, _ = some()'
right_parts_unused2 = 'x, _, _ = some()'
right_parts_unused3 = '_, x, _ = some()'
right_parts_unused4 = '_, _, x = some()'

# regression 1827
right_class_reassignment = """
MyValue = 1

class MyClass(object):
    MyValue = MyValue
"""

# regression 1807
right_tuplelize1 = 'my_var = (my_var,)'
right_tuplelize2 = 'my_var = (other,)'
right_tuplelize3 = 'my_var = (my_var, my_var)'
right_tuplelize4 = 'my_var = (my_var, other)'
right_tuplelize5 = 'my_var = (other, my_var)'

# regression 1874
right_swap1 = 'dx, dy = -dy, dx'
right_swap2 = 'dy, dx = dx, -dy'
right_swap3 = 'dx, dy = --dy, dx'
right_swap4 = 'dx, dy = +dy, -dx'
right_swap5 = 'dx, dy = dy, dx'
right_swap6 = 'dy, dx = dx, dy'

right_unary1 = 'a = not a'
right_unary2 = 'a = -a'

# Wrong:

wrong_fragment = """
test_variable = 5
test_variable = test_variable
"""

wrong_typed_fragment = """
test_variable: int = 5
test_variable: int = test_variable
"""

wrong_partial_typed_fragment1 = """
test_variable: int = 5
test_variable = test_variable
"""

wrong_partial_typed_fragment2 = """
test_variable = 5
test_variable: int = test_variable
"""

wrong_fragment_double_assignment = """
test_variable = 5
test_variable = test_variable = 10
"""

wrong_fragment_double_typed_assignment = """
test_variable: int = 5
test_variable = test_variable = 10
"""

wrong_fragment_other_assignment = """
test_variable = 5
test_variable = other = test_variable = 5
"""

wrong_fragment_typed_other_assignment = """
test_variable: int = 5
test_variable = other = test_variable = 5
"""

wrong_fragment_mixed_tuple_assignment = """
x = 1
y = 2
z = 3
x, y, z = x, z, y
"""

# regression 1812
wrong_parts_unused1 = 'x, _num, _num = some()'

# Double wrong:

wrong_fragment_tuple_assignment = """
x = 1
y = 2
x, y = x, y
"""

wrong_fragment_typed_tuple_assignment = """
x: int = 1
y: int = 2
x, y = x, y
"""

# Triple wrong

wrong_fragment_multiple_tuple_assignment = """
x = 1
y = 2
z = 3
x, y, z = x, y, z
"""

wrong_fragment_typed_multiple_assignment = """
x: int = 1
y: int = 2
z = 3
x, y, z = x, y, z
"""


@pytest.mark.parametrize('code', [
    wrong_fragment,
    wrong_typed_fragment,
    wrong_partial_typed_fragment1,
    wrong_partial_typed_fragment2,
    wrong_fragment_double_assignment,
    wrong_fragment_double_typed_assignment,
    wrong_fragment_other_assignment,
    wrong_fragment_typed_other_assignment,
    wrong_fragment_mixed_tuple_assignment,
    wrong_parts_unused1,
])
def test_self_variable_reassignment(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that self variable reassignment is restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongVariableAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ReassigningVariableToItselfViolation])


@pytest.mark.parametrize('code', [
    wrong_fragment_tuple_assignment,
    wrong_fragment_typed_tuple_assignment,
])
def test_self_variable_reassignment_double(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that self variable reassignment is restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongVariableAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        ReassigningVariableToItselfViolation,
        ReassigningVariableToItselfViolation,
    ])


@pytest.mark.parametrize('code', [
    wrong_fragment_multiple_tuple_assignment,
    wrong_fragment_typed_multiple_assignment,
])
def test_self_variable_reassignment_triple(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that self variable reassignment is restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongVariableAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        ReassigningVariableToItselfViolation,
        ReassigningVariableToItselfViolation,
        ReassigningVariableToItselfViolation,
    ])


@pytest.mark.parametrize('code', [
    right_fragment,
    right_typed_fragment,
    right_just_types,
    right_fragment_tuple_assignment,
    right_fragment_triple_tuple_assignment,
    right_star_assignment1,
    right_star_assignment2,
    right_star_assignment3,
    right_parts_unused1,
    right_parts_unused2,
    right_parts_unused3,
    right_parts_unused4,
    right_class_reassignment,
    right_tuplelize1,
    right_tuplelize2,
    right_tuplelize3,
    right_tuplelize4,
    right_tuplelize5,
    right_swap1,
    right_swap2,
    right_swap3,
    right_swap4,
    right_swap5,
    right_swap6,
    right_unary1,
    right_unary2,
])
def test_correct_variable_reassignment(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that we can do normal variable."""
    tree = parse_ast_tree(code)

    visitor = WrongVariableAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
