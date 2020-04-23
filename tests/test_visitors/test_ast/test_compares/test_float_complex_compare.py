import pytest

from wemake_python_styleguide.violations.best_practices import (
    FloatComplexCompareViolation,
)
from wemake_python_styleguide.visitors.ast.compares import (
    WrongFloatComplexCompareVisitor,
)


@pytest.mark.parametrize('code', [
    '3.0 > 2.0 + 1.0',
    'f2/f1 != 1.0',
    '3.0 in item_list',
    '2.0 < x < 3.0',
    '5.0 not in abc_list',
    '3.0 == 0.1*3',
    '2j != (0.2j)/0.1',
    '2j in comp_list',
    '1j != 2 != 3.0',
    'x == 4.0j',
])
def test_float_complex_compare(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that compares with ``float`` and ``complex`` raise violations."""
    tree = parse_ast_tree(code)

    visitor = WrongFloatComplexCompareVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [FloatComplexCompareViolation])


@pytest.mark.parametrize('code', [
    'x > 3',
    'x <= y',
    'abs(x - y) <= eps',
    'isclose(x, 5.0)',
    'isclose(y, 3j)',
    '3 in item_list',
    '3 != 5',
    '3.0 + x',
    '4.5 + y > z',
])
def test_correct_compares(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing safe compares."""
    tree = parse_ast_tree(code)

    visitor = WrongFloatComplexCompareVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
