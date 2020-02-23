# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    InconsistentReturnVariableViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import (
    ConsistentReturningVariableVisitor,
)

# Correct:

correct_example1 = """
def some_function():
    return 1
"""

correct_example2 = """
def some_function():
    some_value = 1
    other_value = 2
    return some_value + other_value
"""

correct_example3 = """
def some_function():
    some_value = 1
    name = last_name + some_value
    return name, some_value
"""

correct_example4 = """
def some_function():
    some_value = 1
    some_value += 1
    return some_value
"""

correct_example5 = """
def some_function():
    some_value = []
    some_value.append(1)
    return some_value
"""

correct_example6 = """
def foo():
    x, _ = some_tuple
    return x
"""

correct_example7 = """
def foo():
    x.id += some_tuple
    return x.id
"""

correct_example8 = """
def foo():
    x[0]: int = s[0]
    return x[0]
"""

correct_example9 = """
def foo():
    x.attr = 1
    return x.attr
"""

# Regression to 1116
# https://github.com/wemake-services/wemake-python-styleguide/issues/1116
correct_example10 = """
def foo():
    x.attr = 1
    print()
    return x.attr
"""

# Regression to 1116
# https://github.com/wemake-services/wemake-python-styleguide/issues/1116
correct_example11 = """
def foo():
    attr = 1
    print()
    return attr
"""

correct_example12 = """
def some():
    if something:
        return something
"""

correct_example13 = """
def some():
    if something:
        other = 1
        return something
"""

correct_example14 = """
def some():
    other = 2
    if something:
        other = 1
    else:
        return other
"""

correct_example15 = """
def some():
    return some
"""

correct_example16 = """
def some():
    x = 1
    return
"""

correct_example17 = """
def some():
    x, y = 1
    return y, x
"""

correct_example18 = """
def some():
    x, y, z = 1, 2, 3
    return x, y
"""

correct_example19 = """
def some():
    x, y, z = 1, 2, 3
    return y, z
"""

correct_example20 = """
def some():
    x, y, z = 1, 2, 3
    return 0, y, z
"""

correct_example21 = """
def some():
    x, y, z = 1, 2, 3
    return x, y, z, 0
"""

correct_example22 = """
def some():
    x, y, z = some
    return x(), y, z
"""

correct_example23 = """
def some():
    x, y, z = some
    return x[0], y, z
"""

# Wrong:

wrong_example1 = """
def function():
    some_value = 1
    return some_value
"""

wrong_example2 = """
def some_function():
    some_value = 1

    return some_value
"""

wrong_example3 = """
def some_function():
    some_value: int = 1
    return some_value
"""

# Regression to 598
# https://github.com/wemake-services/wemake-python-styleguide/issues/598
wrong_example4 = """
def foo():
    function_result = function(*args, **kwargs)
    return function_result
"""

# Regression to 674
# https://github.com/wemake-services/wemake-python-styleguide/issues/674
wrong_example5 = """
def report_progress(function):
    def decorator(*args, **kwargs):
        function_result = function(*args, **kwargs)
        return function_result
    return decorator
"""

# ifs

wrong_example6 = """
def wrong_if():
    if something:
        other = 1
        return other
"""

wrong_example7 = """
def wrong_if():
    if something:
        ...
    else:
        other = 1
        return other
"""

# fors

wrong_example8 = """
def wrong_for():
    for i in something:
        other = i
        return other
"""

wrong_example9 = """
def wrong_for():
    for i in something:
        ...
    else:
        other = 0
        return other
"""

# whiles

wrong_example10 = """
def wrong_while():
    while something:
        other = 1
        return other
"""

wrong_example11 = """
def wrong_while():
    while something:
        ...
    else:
        other = 2
        return other
"""

# tries

wrong_example12 = """
def wrong_try():
    try:
        other = 1
        return other
    except:
        ...
"""

wrong_example13 = """
def wrong_try():
    try:
        ...
    except:
        other = 1
        return other
"""

wrong_example14 = """
def wrong_try():
    try:
        ...
    except:
        ...
    else:
        other = 1
        return other
"""

wrong_example15 = """
def wrong_try():
    try:
        ...
    finally:
        other = 1
        return other
"""

# tuples

wrong_example16 = """
def wrong_try():
    x, y, z = 1, 2, 3
    return x, y, z
"""

wrong_example16 = """
def wrong_try():
    x, y, z = 1, 2, 3
    return x, y, z
"""

# double

double_wrong_example1 = """
def some():
    if something() == 1:
        some = 1
        return some
    else:
        other = 2
        return other
"""


@pytest.mark.parametrize('code', [
    wrong_example1,
    wrong_example2,
    wrong_example3,
    wrong_example4,
    wrong_example5,
    wrong_example6,
    wrong_example7,
    wrong_example8,
    wrong_example9,
    wrong_example10,
    wrong_example11,
    wrong_example12,
    wrong_example13,
    wrong_example14,
    wrong_example15,
])
def test_wrong_return_variable(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing incorrect `return` statements."""
    tree = parse_ast_tree(mode(code))
    visitor = ConsistentReturningVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [InconsistentReturnVariableViolation])


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
    correct_example14,
    correct_example15,
    correct_example16,
    correct_example17,
    correct_example18,
    correct_example19,
    correct_example20,
    correct_example21,
    correct_example22,
    correct_example23,
])
def test_correct_return_statements(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing correct `return` statements."""
    tree = parse_ast_tree(mode(code))
    visitor = ConsistentReturningVariableVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])


def test_double_wrong_return_variable(
    assert_errors,
    parse_ast_tree,
    default_options,
    mode,
):
    """Testing double incorrect `return` statements."""
    tree = parse_ast_tree(mode(double_wrong_example1))

    visitor = ConsistentReturningVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        InconsistentReturnVariableViolation,
        InconsistentReturnVariableViolation,
    ])
