import pytest

from wemake_python_styleguide.compat.constants import PY39
from wemake_python_styleguide.violations.best_practices import (
    NewStyledDecoratorViolation,
)
from wemake_python_styleguide.visitors.ast.decorators import (
    WrongDecoratorVisitor,
)

_reason = 'new-styled decorators appeared in 3.9'
_mark = pytest.mark.skipif(not PY39, reason=_reason)

function_def = """
@{0}
def some(): ...
"""

method_def = """
class Some(object):
    @{0}
    def some(self): ...
"""


@pytest.mark.parametrize('code', [
    pytest.param(
        function_def,
        marks=_mark,
    ),
    pytest.param(
        method_def,
        marks=_mark,
    ),
])
@pytest.mark.parametrize('decorator', [
    'some[1]',
    'some.attr[0]',
    'some[0].attr',
    'call()[1].attr',

    'some + other',
    'really @ strange[0]',
])
def test_invalid_decorators(
    assert_errors,
    parse_ast_tree,
    code,
    decorator,
    default_options,
    mode,
):
    """Testing that complex decorators are not allowed."""
    tree = parse_ast_tree(mode(code.format(decorator)))

    visitor = WrongDecoratorVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NewStyledDecoratorViolation])


@pytest.mark.parametrize('code', [
    function_def,
    method_def,
])
@pytest.mark.parametrize('decorator', [
    'some',
    'some()',
    'some(index[1])',
    'some.attr',
    'some.attr(1 + 1)',
])
def test_valid_decorators(
    assert_errors,
    parse_ast_tree,
    code,
    decorator,
    default_options,
    mode,
):
    """Testing that conditionals work well."""
    tree = parse_ast_tree(mode(code.format(decorator)))

    visitor = WrongDecoratorVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
