# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.complexity import (
    TooManyContextManagerAssignmentsViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.counts import (
    ContextManagerVisitor,
)

incorrect_count = """
with open('') as first, second:
    ...
"""


@pytest.mark.parametrize('code', [
    incorrect_count,
])
def test_context_manager_multiple_targets(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing incorrect count context manager assignment."""
    tree = parse_ast_tree(code)

    visitor = ContextManagerVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyContextManagerAssignmentsViolation])


correct_count = """
with open('') as first:
    ...
"""


@pytest.mark.parametrize('code', [
    correct_count,
])
def test_context_manager_alone_target(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing correct count context manager assignment."""
    tree = parse_ast_tree(code)

    visitor = ContextManagerVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
