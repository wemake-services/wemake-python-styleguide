import pytest

from wemake_python_styleguide.violations.consistency import (
    MeaninglessNumberOperationViolation,
    UselessOperatorsViolation,
)
from wemake_python_styleguide.visitors.ast.operators import (
    UselessOperatorsVisitor,
)

usage_template = 'constant {0}'


@pytest.mark.parametrize(
    'expression',
    [
        # Math ops:
        '*= 0',
        '**= -0.0',
        '+= 0e0',
        '-= -0b0',
        '* 0',
        '** -0.0',
        '+ 0o0',
        '- -0x0',
        '*= 1',
        '**= 1.0',
        '/= 1',
        '/= 0o1',
        '%= 1',
        '* 0b1',
        '** 1',
        '/ 1.0',
        '% 0o1',
        '* other / 1.0',
        '* 1 * other',
        # Bitwise ops:
        '>> 0',
        '<< 0',
        '| 0b0',
        '^ 0x0',
        '& -0o0',
        '>>= 0',
        '<<= 0',
        '|= 0b0',
        '^= 0x0',
        '&= -0o0',
    ],
)
def test_meaningless_math(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that meaningless number operations are forbidden."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = UselessOperatorsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MeaninglessNumberOperationViolation])


@pytest.mark.parametrize(
    'expression',
    [
        # Math ops:
        '*= -1',
        '*= 10',
        '+= 1e2',
        '-= -0b1',
        '*= 0.1',
        '**= 1.1',
        '/= 0o2',
        '* 0b11',
        '** 2',
        '/ -1.0',
        '* other / 1.5',
        '* -1 * other',
        # Bitwise ops:
        '>> 10',
        '<< 1',
        '| 0b1',
        '^ 2',
        '^= 0x1',
        '& -1',
        '>>= 10',
        '<<= 1',
        '|= 0b1',
        '&= -0o1',
    ],
)
def test_useful_math(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that useful math operations are allowed."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = UselessOperatorsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'expression',
    [
        '6 & 6',
        '1 & True',
        '(not -3) | (not -3)',
        '-~8 ^ -~8',
        '+7 & +++7',
        '-~-7 | -~-7',
        '(not not --7) ^ 7',
    ],
)
def test_meaningless_symmetric_bitwise_math(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that symmetric bitwise operations are forbidden."""
    tree = parse_ast_tree(expression)

    visitor = UselessOperatorsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [MeaninglessNumberOperationViolation],
        ignored_types=UselessOperatorsViolation,
    )


@pytest.mark.parametrize(
    'expression',
    [
        '7 ^ -7',
        '5 & 6',
        '(not -2) | 3',
        '-~7 ^ -~8',
        'value | 2',
        '-value & -3',
        'value ^ -1',
        '+6 & +++7',
        '-~-4 | -~-7',
        '(not not --8) ^ 7',
        'value | ~~4',
    ],
)
def test_useful_asymmetric_bitwise_math(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that asymmetric bitwise operations are allowed."""
    tree = parse_ast_tree(expression)

    visitor = UselessOperatorsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [], ignored_types=UselessOperatorsViolation)


@pytest.mark.parametrize(
    'expression',
    [
        '1 / other',
        '1 / 11',
        '1 / 1.1',
        '1.0 / number',
        '2 // other',
    ],
)
def test_one_to_divide(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that `1 / any number` is the correct expression."""
    tree = parse_ast_tree(expression)

    visitor = UselessOperatorsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'expression',
    [
        '1 / 1',
        '2 / 1',
        '3.3 / 1',
        'other / 1',
        'other // 1',
    ],
)
def test_divide_by_one(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing an error when we divide by one."""
    tree = parse_ast_tree(expression)

    visitor = UselessOperatorsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MeaninglessNumberOperationViolation])
