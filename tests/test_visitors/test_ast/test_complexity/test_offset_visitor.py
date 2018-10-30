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
        some_call()
    except Exception:
        raise
"""

nested_try2 = """
def container():
    if some_call:
        try:
            some_call()
        except Exception:
            raise
"""

nested_with = """
def container():
    with open('some') as temp:
        temp.read()
"""

nested_while = """
def container():
    while True:
        continue
"""

real_nested_values = """
def container():
    if some > 1:
        if some > 2:
            if some > 3:
                if some > 4:
                    if some > 5:
                        print(some)
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
def test_nested_offset(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that nested expression with default options works well."""
    tree = parse_ast_tree(mode(code))

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
    monkeypatch,
    assert_errors,
    parse_ast_tree,
    code,
    number_of_errors,
    default_options,
    mode,
):
    """Testing that nested expressions are restricted."""
    tree = parse_ast_tree(mode(code))

    monkeypatch.setattr(OffsetVisitor, '_max_offset_blocks', 1)
    visitor = OffsetVisitor(default_options, tree=tree)
    visitor.run()

    errors = [TooDeepNestingViolation for _ in range(number_of_errors)]
    assert_errors(visitor, errors)


@pytest.mark.parametrize('code', [
    nested_if,
    nested_if2,
    nested_for,
    nested_with,
    nested_while,
])
def test_nested_offset_error_text(
    monkeypatch,
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that nested expressions are restricted."""
    tree = parse_ast_tree(mode(code))

    monkeypatch.setattr(OffsetVisitor, '_max_offset_blocks', 1)
    visitor = OffsetVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooDeepNestingViolation])
    assert_error_text(visitor, '8')


def test_real_nesting_config(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
    mode,
):
    """Ensures that real configuration works."""
    tree = parse_ast_tree(mode(real_nested_values))

    visitor = OffsetVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooDeepNestingViolation])
    assert_error_text(visitor, '24')


def test_regression282(
    monkeypatch,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """
    Testing that issue-282 will not happen again.

    See: https://github.com/wemake-services/wemake-python-styleguide/issues/282
    """
    tree = parse_ast_tree("""
    async def no_offset():
        ...
    """)

    monkeypatch.setattr(OffsetVisitor, '_max_offset_blocks', 1)
    visitor = OffsetVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
