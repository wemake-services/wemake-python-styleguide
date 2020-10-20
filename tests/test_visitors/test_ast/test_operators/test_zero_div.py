import pytest

from wemake_python_styleguide.violations.consistency import (
    ZeroDivisionViolation,
)
from wemake_python_styleguide.visitors.ast.operators import (
    UselessOperatorsVisitor,
)

usage_template = 'constant {0}'


@pytest.mark.parametrize('expression', [
    '/= 0',
    '/= 0.0',
    '/= -0',
    '/= -0.0',
    '/= -0b0',
    '/= 0b0',
    '/= 0x0',
    '/= -0x0',
    '/= 0o0',
    '/= -0o0',
    '/= 0e0',
    '/= -0e0',
    '//= 0',

    '/ 0',
    '/ 0.0',
    '/ -0',
    '/ -0.0',
    '/ -0b0',
    '/ 0b0',
    '/ 0x0',
    '/ -0x0',
    '/ 0o0',
    '/ -0o0',
    '/ 0e0',
    '/ -0e0',
    '// 0',

    '* other / 0',
    '/ 0 * other',
])
def test_zero_div(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that divisions by zero are forbidden."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = UselessOperatorsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ZeroDivisionViolation])


@pytest.mark.parametrize('expression', [
    '%= 0',
    '%= 0.0',
    '%= -0',
    '%= -0.0',
    '%= -0b0',
    '%= 0b0',
    '%= 0x0',
    '%= -0x0',
    '%= 0o0',
    '%= -0o0',
    '%= 0e0',
    '%= -0e0',

    '% 0',
    '% 0.0',
    '% -0',
    '% -0.0',
    '% -0b0',
    '% 0b0',
    '% 0x0',
    '% -0x0',
    '% 0o0',
    '% -0o0',
    '% 0e0',
    '% -0e0',

    '* other % 0',
    '% 0 * other',
])
def test_zero_mod(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that useless modulus with zero are forbidden."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = UselessOperatorsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ZeroDivisionViolation])


@pytest.mark.parametrize('expression', [
    # Div, but not with zero:
    '/= 0.1',
    '/= -1.0',
    '/= -10',
    '/= -100.0',
    '/= 0b101',
    '/= -1e0',
    '//= 9',

    '/ 10',
    '/ 0.01',
    '/ -0.2',
    '/ -0x11',

    # variables:
    '* var',
    '- var',
    '/ var',
    '+ var',
    '% var',
    '*= var',
    '-= var',
    '/= var',
    '+= var',
    '%= var',
])
def test_correct_zero_div(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that non-zero divisions are allowed."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = UselessOperatorsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('expression', [
    # Mod, but not with zero:
    '%= 0.1',
    '%= -1.0',
    '%= -10',
    '%= -100.0',
    '%= 0b101',
    '%= -1e0',

    '% 10',
    '% 0.01',
    '% -0.2',
    '% -0x11',
])
def test_correct_zero_mod(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that non-zero modulus operations are allowed."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = UselessOperatorsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
