import pytest

from wemake_python_styleguide.compat.constants import PY310, PY311
from wemake_python_styleguide.visitors.ast.complexity.offset import (
    OffsetVisitor,
    TooDeepNestingViolation,
)

nested_if = """
def container():
    if True:
        ...  # this needs to be an ellipsis for the test
"""

nested_if2 = """
def container():
    if some_value:
        call_other()
"""

nested_for = """
def container():
    for i in '123':
        return 0
"""

nested_try = """
def container():
    try:
        some_call()
    except Exception:
        raise
"""

nested_try2 = """
def container():
    if some_call:
        try:
            some_call()
        except Exception:
            raise
"""

nested_try_star = """
def container():
    try:
        ...
    except* ...:
        ...
"""

nested_with = """
def container():
    with open('some') as temp:
        temp.read()
"""

nested_while = """
def container():
    while True:
        continue
"""

nested_match = """
def container():
    match ...:
        case 1:
            ...
"""

real_nested_values = """
def container():
    if some > 1:
        if some > 2:
            if some > 3:
                if some > 4:
                    if some > 5:
                        print(some)
"""

# Regression for #320:
real_await_nested_values = """
async def update_control():
    current_control = await too_long_name_please_find_one({'line': 1,
                                                           'point': 1})
"""

# Only ellipsis in the top level function definition is fine:

top_level_function_ellipsis = """
def function_with_really_long_name(): ...
"""

top_level_method_ellipsis = """
class MyClass:
    def function_with_really_long_name(self): ...
"""


@pytest.mark.parametrize('code', [
    nested_if,
    nested_if2,
    nested_for,
    nested_try,
    nested_try2,
    pytest.param(
        nested_try_star,
        marks=pytest.mark.skipif(
            not PY311,
            reason='ExceptionGroup was added in 3.11',
        ),
    ),
    nested_with,
    nested_while,
    pytest.param(
        nested_match,
        marks=pytest.mark.skipif(
            not PY310,
            reason='Pattern matching was added in 3.10',
        ),
    ),
    top_level_function_ellipsis,
    top_level_method_ellipsis,
])
def test_nested_offset(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that nested expression with default options works well."""
    tree = parse_ast_tree(mode(code))

    visitor = OffsetVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


def test_nested_offset_regression320(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """
    Testing that await works well with long lines.

    See: https://github.com/wemake-services/wemake-python-styleguide/issues/320
    """
    tree = parse_ast_tree(real_await_nested_values)

    visitor = OffsetVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(('code', 'number_of_errors'), [
    (nested_if, 1),
    (nested_if2, 1),
    (nested_for, 1),
    (nested_try, 2),
    (nested_try2, 4),
    (nested_try_star, 2),
    (nested_with, 1),
    (nested_while, 1),
    (nested_match, 1),
])
def test_nested_offset_errors(
    monkeypatch,
    assert_errors,
    parse_ast_tree,
    code,
    number_of_errors,
    default_options,
    mode,
):
    """Testing that nested expressions are restricted."""
    if code == nested_try_star and not PY311:
        pytest.skip(reason='ExceptionGroup was added in 3.11')
    if code == nested_match and not PY310:
        pytest.skip(reason='Pattern matching was added in 3.10')

    tree = parse_ast_tree(mode(code))

    monkeypatch.setattr(OffsetVisitor, '_max_offset_blocks', 1)
    visitor = OffsetVisitor(default_options, tree=tree)
    visitor.run()

    errors = [TooDeepNestingViolation for _ in range(number_of_errors)]
    assert_errors(visitor, errors)


@pytest.mark.parametrize('code', [
    nested_if,
    nested_if2,
    nested_for,
    nested_with,
    nested_while,
])
def test_nested_offset_error_text(
    monkeypatch,
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that nested expressions are restricted."""
    tree = parse_ast_tree(mode(code))

    monkeypatch.setattr(OffsetVisitor, '_max_offset_blocks', 1)
    visitor = OffsetVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooDeepNestingViolation])
    assert_error_text(visitor, '8', 4)


def test_real_nesting_config(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
    mode,
):
    """Ensures that real configuration works."""
    tree = parse_ast_tree(mode(real_nested_values))

    visitor = OffsetVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooDeepNestingViolation])
    assert_error_text(visitor, '24', 10 * 2)


def test_regression282(
    monkeypatch,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """
    Testing that issue-282 will not happen again.

    See: https://github.com/wemake-services/wemake-python-styleguide/issues/282
    """
    code = """
    async def no_offset():
        ...
    """
    tree = parse_ast_tree(code)

    monkeypatch.setattr(OffsetVisitor, '_max_offset_blocks', 1)
    visitor = OffsetVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
