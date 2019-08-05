# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    ListMultiplyViolation,
)
from wemake_python_styleguide.visitors.ast.operators import (
    WrongMathOperatorVisitor,
)

usage_template = 'constant = {0}'


@pytest.mark.parametrize('expression', [
    '[] * 1',
    '[1] * 2',
    '[1, 2] * 0',
    '[x for x in ()] * 1.1',
    '[[] * 2 for x in some]',
])
def test_list_mult_operation(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that list multiplies are forbidden."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = WrongMathOperatorVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ListMultiplyViolation])


@pytest.mark.parametrize('expression', [
    '1 * 2',
    '() * 1',
    '[1, 2] + [3, 4]',
    '[x * 1 for x in some]',
    '[x * 1 for x in some] + [2 * x for x in some]',
])
def test_correct_list_operation(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that non lists are allowed."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = WrongMathOperatorVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
