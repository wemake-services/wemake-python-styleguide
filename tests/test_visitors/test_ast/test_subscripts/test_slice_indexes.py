import pytest

from wemake_python_styleguide.violations.best_practices import (
    ComplexSliceIndexViolation,
)
from wemake_python_styleguide.visitors.ast.subscripts import SliceIndexVisitor

usage_template = 'constant[{0}]'


@pytest.mark.parametrize(
    'expression',
    [
        'my_dict["start_index"]:',
        '::my_dict["step"]',
        'my_list[0]:',
        '::my_list[-1]',
        'start_index():',
        '::step()',
        'Slice().start:',
        'Slice(arg_1).start:',
        'index.start():',
        ':-(-x + 1)',
        ':-(-x + -y)',
        ':-(-x + -(y + 1))',
        ':-(-(x + 1) + -(y + 1))',
        '(1 - (x + 2)):',
        '(1 - (x + 2) * 2):',
        '(index.start + 1):',
        '(x + y + z):',
        ':x + y + z',
    ],
)
def test_invalid_slice_indexes(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that invalid indexes are forbidden."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = SliceIndexVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ComplexSliceIndexViolation])


@pytest.mark.parametrize(
    'expression',
    [
        '1:3',
        '1:3:2',
        'start:end',
        '::step',
        'index.start:',
        'index.start::index.step',
        'Slice.start:',
        ':-start',
        '(x + 1):',
        '(-x + 1):',
        ':-(x + 1)',
        '::-index.step',
    ],
)
def test_valid_slice_indexes(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that valid indexes are allowed."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = SliceIndexVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
