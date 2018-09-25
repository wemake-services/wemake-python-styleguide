# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.complexity.counts import (
    ConditionsVisitor,
    TooManyConditionsViolation,
)

empty_module = ''

condition_with_single_if = """
if 4 > 2 and 3 / 2 == 1.5:
    print(1)
"""

condition_with_single_if_multiline = """
if (
    some_call() or default_value
):
    print(1)
"""

condition_with_several_ifs = """
if True or False:
    print(1)
if True:
    print(2)
"""

condition_with_several_elifs = """
if True and False:
    print(1)
elif False:
    print(2)
"""

condition_inline = 'some_value = 12 if True and 4 > 3 else 0'
condition_with_inline_for = 'nodes = [node for node in html if 1 and 2 > 1]'
condition_with_simple_inline_for = 'nodes = [node for node in html]'

while_with_condition = """
while True and 1 == 1:
    print(1)
"""


@pytest.mark.parametrize('code', [
    empty_module,
    condition_with_single_if,
    condition_with_single_if_multiline,
    condition_with_several_ifs,
    condition_with_several_elifs,
    condition_inline,
    condition_with_inline_for,
    condition_with_simple_inline_for,
    while_with_condition,
])
def test_module_condition_counts_normal(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that conditions in a module work well."""
    tree = parse_ast_tree(code)

    visitor = ConditionsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    condition_with_single_if,
    condition_with_single_if_multiline,
    condition_with_several_ifs,
    condition_with_several_elifs,
    condition_inline,
    condition_with_inline_for,
    while_with_condition,
])
def test_module_condition_counts_violation(
    assert_errors, parse_ast_tree, code, options,
):
    """Testing that violations are raised when reaching max value."""
    tree = parse_ast_tree(code)

    option_values = options(max_conditions=1)
    visitor = ConditionsVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyConditionsViolation])
