# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    OpeationSignNegationViolation,
)
from wemake_python_styleguide.visitors.ast.operators import (
    WrongMathOperatorVisitor,
)

usage_template = 'constant {0}'


@pytest.mark.parametrize('expression', [
    '- -1',
    '- -0.1',
    '- -num',
    '- -0b0',
    '- -0x0',
    '- -0o4',
    '- -1e1',

    '+ -1',
    '+ -0.1',
    '+ -num',
    '+ -0b0',
    '+ -0x0',
    '+ -0o4',
    '+ -1e1',

    '-= -1',
    '-= -0.1',
    '-= -num',
    '-= -0b0',
    '-= -0x0',
    '-= -0o4',
    '-= -1e1',

    '+= -1',
    '+= -0.1',
    '+= -num',
    '+= -0b0',
    '+= -0x0',
    '+= -0o4',
    '+= -1e1',
])
def test_minus_minus_operation(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that negated operations are forbidden."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = WrongMathOperatorVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [OpeationSignNegationViolation])


@pytest.mark.parametrize('expression', [
    '- 1',
    '* -0.1',
    '/ -num',
    '+ 0b0',
    '- ~1',

    '*= -1',
    '*= 0.1',
    '**= -num',
    '/= -0b0',
    '^= -0x0',
    '-= 0o4',
    '-= ~1e1',
])
def test_correct_operation(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that non-negated operations are allowed."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = WrongMathOperatorVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
