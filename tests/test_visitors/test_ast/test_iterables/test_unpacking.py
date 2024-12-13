import pytest

from wemake_python_styleguide.compat.constants import PY311
from wemake_python_styleguide.violations.consistency import (
    IterableUnpackingViolation,
)
from wemake_python_styleguide.visitors.ast.iterables import (
    IterableUnpackingVisitor,
)

_skip_mark = pytest.mark.skipif(
    not PY311,
    reason='Unpacking in subscript is only allow in 3.11+',
)

args_unpacking_in_call = 'f(*args)'
spread_list_definition = '[1, 2, *numbers, 74]'
spread_set_definition = '{1, 2, *numbers, 74}'
spread_tuple_definition = '(1, 2, *numbers, 74)'
spread_assignment = 'first, *_ = [1, 2, 4, 3]'
type_annotation1 = 'first: Tuple[*Shape]'
type_annotation2 = 'first: tuple[*Shape]'
type_alias = 'first = Tuple[*Shape]'
generic_type = 'class MyClass(Generic[*Shape]): ...'
similar_but_unrelated = 'my_obj[*my_iter]'

wrong_list_definition = '[*numbers]'
wrong_set_definition = '{*numbers}'
wrong_tuple_definition = '(*numbers,)'
wrong_spread_assignment = '*_, = [1, 2, 4, 3]'


@pytest.mark.parametrize(
    'code',
    [
        args_unpacking_in_call,
        spread_list_definition,
        spread_set_definition,
        spread_tuple_definition,
        spread_assignment,
        # Type annotations should be allowed:
        pytest.param(type_annotation1, marks=_skip_mark),
        pytest.param(type_annotation2, marks=_skip_mark),
        pytest.param(type_alias, marks=_skip_mark),
        pytest.param(generic_type, marks=_skip_mark),
        # As a side-effect of type annotations,
        # we also allow this code in runtime:
        pytest.param(similar_but_unrelated, marks=_skip_mark),
    ],
)
def test_correct_iterable_unpacking_usage(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that correct iterable unpacking is allowed."""
    tree = parse_ast_tree(code)

    visitor = IterableUnpackingVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        wrong_list_definition,
        wrong_set_definition,
        wrong_tuple_definition,
        wrong_spread_assignment,
    ],
)
def test_unnecessary_iterable_unpacking_usage(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that unnecessary iterable unpacking is restricted."""
    tree = parse_ast_tree(code)

    visitor = IterableUnpackingVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [IterableUnpackingViolation])
