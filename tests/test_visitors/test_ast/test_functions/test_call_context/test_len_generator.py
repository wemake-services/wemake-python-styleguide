import pytest

from wemake_python_styleguide.violations.refactoring import (
    LenGeneratorViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    WrongFunctionCallContextVisitor,
)

template = """
def function():
    {0}
"""

wrong_samples = (
    'len(x for x in items)',
    'len(number for number in range(10))',
)


@pytest.mark.parametrize(
    'code',
    [
        'len([x for x in items])',
        'len((1, 2, 3))',
        'len([])',
        'len(some)',
        'len(range(10))',
    ],
)
def test_correct_len_generator(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that valid uses of ``len()`` are allowed."""
    tree = parse_ast_tree(mode(template.format(code)))

    visitor = WrongFunctionCallContextVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', wrong_samples)
def test_len_generator(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that ``len(generator)`` is forbidden."""
    tree = parse_ast_tree(mode(template.format(code)))

    visitor = WrongFunctionCallContextVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [LenGeneratorViolation])