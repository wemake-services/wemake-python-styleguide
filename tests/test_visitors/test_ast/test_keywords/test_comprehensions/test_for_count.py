# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.keywords import (
    TooManyForsInComprehensionViolation,
    WrongComprehensionVisitor,
)

regular_loop_comprehension = """
nodes = [
    target
    for assignment in top_level_assigns
    for target in assignment.targets
]
"""

complex_loop_comprehension = """
nodes = [
    target
    for assignment in top_level_assigns
    for target in assignment.targets
    for _ in range(10)
]
"""

regular_dict_comprehension = """
nodes = {
    target: 1
    for assignment in top_level_assigns
    for target in assignment.targets
}
"""

complex_dict_comprehension = """
nodes = {
    target: 1
    for assignment in top_level_assigns
    for target in assignment.targets
    for _ in range(10)
}
"""

regular_gen_expression = """
nodes = (
    target
    for assignment in top_level_assigns
    for target in assignment.targets
)
"""

complex_gen_expression = """
nodes = (
    target
    for assignment in top_level_assigns
    for target in assignment.targets
    for _ in range(10)
)
"""

regular_nested_list_comprehension = """
def container():
    nodes = [
        target
        for assignment in top_level_assigns
        for target in assignment.targets
    ]
"""

complex_nested_list_comprehension = """
def container():
    nodes = [
        target
        for assignment in top_level_assigns
        for target in assignment.targets
        for _ in range(10)
    ]
"""


@pytest.mark.parametrize('code', [
    complex_loop_comprehension,
    complex_dict_comprehension,
    complex_gen_expression,
])
def test_multiple_for_keywords_in_comprehension(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that using multiple `for` keywords is restricted."""
    tree = parse_ast_tree(code)
    visitor = WrongComprehensionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyForsInComprehensionViolation])


@pytest.mark.parametrize('code', [
    complex_nested_list_comprehension,
])
def test_multiple_fors_in_async_comprehension(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that using multiple `for` keywords is restricted."""
    tree = parse_ast_tree(mode(code))
    visitor = WrongComprehensionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyForsInComprehensionViolation])


@pytest.mark.parametrize('code', [
    regular_loop_comprehension,
    regular_dict_comprehension,
    regular_gen_expression,
])
def test_regular_fors_in_comprehension(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that using two `for` keywords is allowed."""
    tree = parse_ast_tree(code)
    visitor = WrongComprehensionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    regular_nested_list_comprehension,
])
def test_regular_fors_in_async_comprehension(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that using two `for` keywords is allowed."""
    tree = parse_ast_tree(mode(code))
    visitor = WrongComprehensionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
