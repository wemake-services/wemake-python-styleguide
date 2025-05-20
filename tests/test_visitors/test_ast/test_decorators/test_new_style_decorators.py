import pytest

from wemake_python_styleguide.compat.constants import PY312
from wemake_python_styleguide.violations.best_practices import (
    NewStyledDecoratorViolation,
)
from wemake_python_styleguide.visitors.ast.decorators import (
    WrongDecoratorVisitor,
)

function_def = """
@{0}
def some(): ...
"""

method_def = """
class Some:
    @{0}
    def some(self): ...
"""

invalid_decorators = [
    'some[1]',
    'some.attr[0]',
    'some[0].attr',
    'call()[1].attr',
    'some + other',
    'really @ strange[0]',
]

valid_decorators = [
    'some',
    'some()',
    'some(index[1])',
    'some.attr',
    'some.attr(1 + 1)',
]

invalid_decorators3_12 = [
    'some + other',
    'some[1] + other[1]',
    'some.attr + other.attr',
    'some[0].attr + other.attr[0]',
    'really @ strange[0]',
]

valid_decorators3_12 = [
    *valid_decorators,
    'some[my_type]',
    'some[my_type](index)',
    'some.attr[my_type]()',
    'some.attr(1)[my_type]',
]


@pytest.mark.parametrize(
    'code',
    [
        function_def,
        method_def,
    ],
)
@pytest.mark.parametrize(
    'decorator',
    invalid_decorators3_12 if PY312 else invalid_decorators,
)
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


@pytest.mark.parametrize(
    'code',
    [
        function_def,
        method_def,
    ],
)
@pytest.mark.parametrize(
    'decorator',
    valid_decorators3_12 if PY312 else valid_decorators,
)
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
