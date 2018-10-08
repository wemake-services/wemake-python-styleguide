# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    ConstantComparisonViolation,
)
from wemake_python_styleguide.visitors.ast.comparisons import (
    ConstantComparisonVisitor,
)


@pytest.mark.parametrize('code', [
    'foo < bar',
    '0 < x < 1',
    '("foo" + "bar") in x',
    '1 in (1, x)',
])
def test_string_normal(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that comparisons work well."""
    tree = parse_ast_tree(code)

    visitor = ConstantComparisonVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    '1 == 1',
    '1 != 0',
    '(1) != 0',
    '0 < 1 < x',
    'x < 0 < 1',
    '[x for x in y if 1 is 2]',
    '(0 == 1) is x',
    '"foo" "bar" in "foobarbaz"',
    'if 1 > 1: pass',
    'if 9 > x and 4 < 2: pass',
    'if 3 < 5 < 10: pass',
])
def test_wrong_string(assert_errors, parse_ast_tree, code, default_options):
    """Testing that violations are raised when reaching max value."""
    tree = parse_ast_tree(code)

    visitor = ConstantComparisonVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ConstantComparisonViolation])
