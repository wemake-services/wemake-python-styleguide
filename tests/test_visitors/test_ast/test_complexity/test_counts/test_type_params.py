import pytest
from wemake_python_styleguide.compat.constants import PY312
from wemake_python_styleguide.violations.complexity import (
    TooManyTypeParams,
)
from wemake_python_styleguide.visitors.ast.complexity.counts import (
    TypeParamsVisitor,
)

if not PY312:
    pytest.skip(reason='type_params was added in 3.12', allow_module_level=True)


type_alias_params6 = 'type Alias[A, B, C, D, E, F] = ...'
type_alias_params7 = 'type Alias[A, B, C, D, E, F, G] = ...'
class_params6 = 'class Class[A, B, C, D, E, F]: ...'
class_params7 = 'class Class[A, B, C, D, E, F, G]: ...'
function_params6 = 'def func[A, B, C, D, E, F](): ...'
function_params7 = 'def func[A, B, C, D, E, F, G](): ...'
async_function_params6 = 'async def func[A, B, C, D, E, F](): ...'
async_function_params7 = 'async def func[A, B, C, D, E, F, G](): ...'


@pytest.mark.parametrize(
    'code',
    [
        type_alias_params7,
        class_params7,
        function_params7,
        async_function_params7,
    ],
)
def test_type_params_wrong_count(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that default settings raise a warning."""
    tree = parse_ast_tree(code)

    visitor = TypeParamsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyTypeParams])
    assert_error_text(visitor, '7', baseline=default_options.max_type_params)


@pytest.mark.parametrize(
    'code',
    [
        type_alias_params6,
        class_params6,
        function_params6,
        async_function_params6,
    ],
)
def test_type_params_correct_count(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that default settings do not raise a warning."""
    tree = parse_ast_tree(code)

    visitor = TypeParamsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        type_alias_params6,
        type_alias_params7,
        class_params6,
        class_params7,
        function_params6,
        function_params7,
        async_function_params6,
        async_function_params7,
    ],
)
def test_type_params_configured_count(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """Testing that settings can reflect the change."""
    tree = parse_ast_tree(code)

    option_values = options(max_type_params=8)
    visitor = TypeParamsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyTypeParams])
