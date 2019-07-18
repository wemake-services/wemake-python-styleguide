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
def test():
     print('test')
"""

correct_example10 = """
def test(some):
     if some:
          return
     print('test')
"""

correct_example11 = """
def test(some):
     if some:
          return some
     print('test')
     return None
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
     name = last_name + first_name
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
   print('Done, result is logged')  # we obviously need this line
   return function_result
"""

# Regression to 674
# https://github.com/wemake-services/wemake-python-styleguide/issues/674
wrong_example5 = """
def report_progress(function):
    def decorator(*args, **kwargs):
        function_result = function(*args, **kwargs)
        print('done!')
        return function_result
    return decorator
"""

wrong_example6 = """
def test():
     print('test')
     return None
"""

wrong_example7 = """
def test():
     print('test')
     return
"""

wrong_example8 = """
def test(some):
     if some:
          return
     print('test')
     return
"""

double_wrong_example1 = """
def some():
   if something() == 1:
       some = 1
       another_some = 'Hello'
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
    wrong_example8
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
