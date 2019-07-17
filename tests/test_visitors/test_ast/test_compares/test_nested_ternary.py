# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    NestedTernaryViolation,
)
from wemake_python_styleguide.visitors.ast.compares import (
    WrongConditionalVisitor,
)

wrong_compare1 = 'x > (a if b else c)'
wrong_compare2 = '(a if b else c) > x'
wrong_compare3 = 'x == (a if b else c)'
wrong_compare4 = '(a if b else c) == x == y'
wrong_compare5 = 'x == (a if b else c) == y'
wrong_compare6 = 'x != (a if b else c)'

wrong_boolop1 = 'x and (a if b else c)'
wrong_boolop2 = 'x or (a if b else c)'
wrong_boolop3 = '(a if b else c) or x'
wrong_boolop4 = 'x and (a if b else c) or y'
wrong_boolop5 = 'x and y or (a if b else c)'
wrong_boolop6 = '(a if b else c) and x or y'

wrong_binop1 = 'x + (a if b else c)'
wrong_binop2 = 'x - (a if b else c)'
wrong_binop3 = '(a if b else c) / y'
wrong_binop4 = 'x + (a if b else c) - y'
wrong_binop5 = 'x + y - (a if b else c)'
wrong_binop6 = '(a if b else c) * x / y'

wrong_unary1 = '+(a if b else c)'
wrong_unary2 = '-(a if b else c)'
wrong_unary3 = '~(a if b else c)'
wrong_unary4 = 'not (a if b else c)'

wrong_if = 'if a if b else c: ...'

# Correct:

correct_if = """
if x:
    y = a if b else c
    print(a if b else c, end=a if b else c)
    d = {'key': a if b else c}
"""

correct_unary1 = '-a if b else c'
correct_unary2 = 'a if -b else c'
correct_unary3 = 'a if b else -c'
correct_unary4 = 'not a if b else c'

correct_binop1 = 'a + x if b else c'
correct_binop2 = 'a if b + x else c'
correct_binop3 = 'a if b else c + x'

correct_boolop1 = 'a and x if b else c'
correct_boolop2 = 'a if b and x else c'
correct_boolop3 = 'a if b else c and x'

correct_compare1 = 'a > x if b else c'
correct_compare2 = 'a if b > x else c'
correct_compare3 = 'a if b else c < x'


@pytest.mark.parametrize('code', [
    correct_if,

    correct_unary1,
    correct_unary2,
    correct_unary3,
    correct_unary4,

    correct_binop1,
    correct_binop2,
    correct_binop3,

    correct_boolop1,
    correct_boolop2,
    correct_boolop3,

    correct_compare1,
    correct_compare2,
    correct_compare3,
])
def test_non_nested_ternary(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that ternary can be used work well."""
    tree = parse_ast_tree(code)

    visitor = WrongConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_compare1,
    wrong_compare2,
    wrong_compare3,
    wrong_compare4,
    wrong_compare5,
    wrong_compare6,

    wrong_boolop1,
    wrong_boolop2,
    wrong_boolop3,
    wrong_boolop4,
    wrong_boolop5,
    wrong_boolop6,

    wrong_binop1,
    wrong_binop2,
    wrong_binop3,
    wrong_binop4,
    wrong_binop5,
    wrong_binop6,

    wrong_unary1,
    wrong_unary2,
    wrong_unary3,
    wrong_unary4,

    wrong_if,
])
def test_nested_ternary(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that ternary can be used work well."""
    tree = parse_ast_tree(code)

    visitor = WrongConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NestedTernaryViolation])
