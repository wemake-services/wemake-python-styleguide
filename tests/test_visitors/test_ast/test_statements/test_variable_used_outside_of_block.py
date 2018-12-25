# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    VariableUsedOutsideOfBlockViolation,
)
from wemake_python_styleguide.visitors.ast.statements import (
    VariableUsedOutsideOfBlockVisitor,
)

variable_used_outside_with = """
def function():
    with a.open() as x:
        some_call()
    print('This is not allowed'.format(x))
"""

multiple_variables_defined_by_with = """
with a.open(), b.open() as c, d.open() as (e, f):
    print("Hello")
print(f)
"""

variable_used_outside_for = """
for ind in range(100):
    print(ind)
total = ind + 1
"""

multiple_variables_defined_by_for = """
for (a, b, c, d) in call(1):
    iterate()
x = c/2
"""

valid_with_usage = """
with a as (b, c):
    print(b)
print(a)
"""


valid_for_usage = """
counter = 0
for a in range(100):
    print(a)
    counter = a
print(counter)
"""


@pytest.mark.parametrize('example,violation', [
    (variable_used_outside_for, [VariableUsedOutsideOfBlockViolation]),
    (multiple_variables_defined_by_for, [VariableUsedOutsideOfBlockViolation]),
    (variable_used_outside_with, [VariableUsedOutsideOfBlockViolation]),
    (multiple_variables_defined_by_with, [VariableUsedOutsideOfBlockViolation]),
    (valid_for_usage, []),
    (valid_with_usage, []),
    ])
def test_detect_violations(
    example,
    violation,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing that detection of variables being used outside of block."""
    tree = parse_ast_tree(example)
    visitor = VariableUsedOutsideOfBlockVisitor(default_options, tree)
    visitor.run()
    assert_errors(visitor, violation)
