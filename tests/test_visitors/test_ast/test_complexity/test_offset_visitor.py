# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.complexity.offset import (
    OffsetVisitor,
    TooDeepNestingViolation,
)

nested_if = """
def container():
    if True:
        x = 1
"""

nested_if2 = """
def container():
    if some_value:
        call_other()
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

nested_try2 = """
def container():
    if some:
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
    nested_if2,
    nested_for,
    nested_try,
    nested_try2,
    nested_with,
    nested_while,
])
def test_nested_offset(assert_errors, parse_ast_tree, code, default_options):
    """Testing that nested expression with default options works well."""
    tree = parse_ast_tree(code)

    visitor = OffsetVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code, number_of_errors', [
    (nested_if, 1),
    (nested_if2, 1),
    (nested_for, 1),
    (nested_try, 2),
    (nested_try2, 4),
    (nested_with, 1),
    (nested_while, 1),
])
def test_nested_offset_errors(
    assert_errors, parse_ast_tree, code, number_of_errors, options,
):
    """Testing that nested expressions are restricted."""
    tree = parse_ast_tree(code)

    option_values = options(max_offset_blocks=1)
    visitor = OffsetVisitor(option_values, tree=tree)
    visitor.run()

    errors = [TooDeepNestingViolation for _ in range(number_of_errors)]
    assert_errors(visitor, errors)
