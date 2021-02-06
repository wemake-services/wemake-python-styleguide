import pytest

from wemake_python_styleguide.violations.best_practices import FloatKeyViolation
from wemake_python_styleguide.visitors.ast.subscripts import CorrectKeyVisitor

usage_template = 'some_dict[{0}]'


@pytest.mark.parametrize('expression', [
    '1.0',
    '-0.0',
    '+3.5',
])
def test_float_key_usage(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that redundant subscripts are forbidden."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = CorrectKeyVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [FloatKeyViolation])


@pytest.mark.parametrize('expression', [
    '5',
    'name',
    'call()',
    'name.attr',
    'name[sub]',
    '...',
    '"str"',
    'b""',
    '3j',
    '5 + 0.1',
    '3 / 2',
])
def test_correct_subscripts(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that non-redundant subscripts are allowed."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = CorrectKeyVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
