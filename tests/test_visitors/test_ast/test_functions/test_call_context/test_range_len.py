import pytest

from wemake_python_styleguide.violations.refactoring import (
    ImplicitEnumerateViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    WrongFunctionCallContextVisitor,
)

for_template = """
def function():
    for list_item in {0}:
        ...
"""

wrong_samples = (
    'range(len())',
    'range(len(some))',
    'range(len([]))',
    'range(1, len(some))',
    'range(-1, len(some))',
    'range(0, len(some), -1)',
)


@pytest.mark.parametrize('code', [
    'range(10)',
    'range(10, 20)',
    'range(0, 10, 1)',
    'range(some())',
    'range(len)',
    'len([])',
    'len(some)',
    'len(range(10))',
    'range(0, len(some), 2)',
    'range(0, len(some), -2)',
])
def test_correct_range_len(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that ``range()`` can be used."""
    tree = parse_ast_tree(mode(for_template.format(code)))

    visitor = WrongFunctionCallContextVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', wrong_samples)
def test_range_len(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that ``range(len(...))`` cannot be used."""
    tree = parse_ast_tree(mode(for_template.format(code)))

    visitor = WrongFunctionCallContextVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ImplicitEnumerateViolation])


@pytest.mark.parametrize('code', wrong_samples)
def test_range_len_outside_for_loop(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that ``range(len(...))`` can be used outside loops."""
    tree = parse_ast_tree(code)

    visitor = WrongFunctionCallContextVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
