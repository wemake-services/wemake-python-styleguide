import pytest

from wemake_python_styleguide.violations.best_practices import (
    FloatingNanViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    FloatingNanCallVisitor,
)


@pytest.mark.parametrize('code', [
    'float(4.5) + 4.2',
    'float(2) + 0',
    'result = "NaN".join(["a", "a"])',
    'a = math.nan',
])
def test_correct_nan_acquisition(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that acquiring NaN in a proper way is not  as a violation."""
    tree = parse_ast_tree(mode(code))

    visitor = FloatingNanCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('prefix', [
    'b',
    'u',
    '',
])
@pytest.mark.parametrize('nan_variant', [
    'NaN',
    'NAN',
    'nan',
    'Nan',
])
@pytest.mark.parametrize('code', [
    'float({0})',
    'float({0}) < 0.0',
    'sorted([5.0, float({0}), 10.0, 0.0])',
])
def test_floating_nan(
    assert_errors,
    parse_ast_tree,
    prefix,
    nan_variant,
    code,
    default_options,
):
    """Testing that "NaN" argument to ``float()`` is as a violation."""
    nan = '{0}"{1}"'.format(prefix, nan_variant)
    tree = parse_ast_tree(code.format(nan))

    visitor = FloatingNanCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [FloatingNanViolation])
