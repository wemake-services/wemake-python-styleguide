# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.complexity.offset import (
    OffsetVisitor,
    TooDeepNestingViolation,
)

nested_if = """
def container():
    if True:
        x = 1
"""

nested_for = """
def container():
    for i in '123':
        return 0
"""

nested_try = """
def container():
    try:
        some()
    except Exception:
        raise
"""

nested_with = """
if True:
    with open('some') as temp:
        temp.read()
"""


nested_while = """
while True:
    while True:
        continue
"""


@pytest.mark.parametrize('code', [
    nested_if,
    nested_for,
    nested_try,
    nested_with,
    nested_while,
])
def test_nested_offset(assert_errors, parse_ast_tree, code, default_options):
    """Testing that nested expression with default options works well."""
    tree = parse_ast_tree(code)

    visiter = OffsetVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [])


@pytest.mark.parametrize('code, number_of_errors', [
    (nested_if, 1),
    (nested_for, 1),
    (nested_try, 2),
    (nested_with, 1),
    (nested_while, 1),
])
def test_nested_offset_errors(
    assert_errors, parse_ast_tree, code, number_of_errors, options,
):
    """Testing that nested expressions are restricted."""
    tree = parse_ast_tree(code)

    option_values = options(max_offset_blocks=1)
    visiter = OffsetVisitor(option_values)
    visiter.visit(tree)

    errors = [TooDeepNestingViolation for _ in range(number_of_errors)]
    assert_errors(visiter, errors)
