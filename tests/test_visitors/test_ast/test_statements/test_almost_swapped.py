# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    AlmostSwappedViolation,
)
from wemake_python_styleguide.visitors.ast.statements import (
    StatementsWithBodiesVisitor,
)

# Correct:

correct_swapped_variables = 'a, b = b, a'

# Wrong:

wrong_swapped_variables = """
a = b
b = a
"""

wrong_swapped_variables_with_temp = """
temp = a
a = b
b = temp
"""


@pytest.mark.parametrize('code', [
    wrong_swapped_variables,
    wrong_swapped_variables_with_temp,
])
def test_wrong_swapped_variables(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Ensures that incorrectly swapped variables are forbidden."""
    tree = parse_ast_tree(code)

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [AlmostSwappedViolation])


@pytest.mark.parametrize('code', [
    correct_swapped_variables,
])
def test_correct_swapped_variables(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that correctly swapped variables."""
    tree = parse_ast_tree(code)

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
