import pytest

from wemake_python_styleguide.violations.consistency import (
    IncorrectYieldFromTargetViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import (
    GeneratorKeywordsVisitor,
)

yield_from_template = """
def wrapper():
    yield from {0}
"""


@pytest.mark.parametrize('code', [
    '()',
    '[1, 2, 3]',
    '[name, other]',
    '{1, 2, 3}',
    '"abc"',
    'b"abc"',
    'a + b',
    '[a for a in some()]',
    '{a for a in some()}',
])
def test_yield_from_incorrect_type(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Ensure that `yield from` does not work with incorrect types."""
    tree = parse_ast_tree(yield_from_template.format(code))

    visitor = GeneratorKeywordsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [IncorrectYieldFromTargetViolation])


@pytest.mark.parametrize('code', [
    'name',
    'name.attr',
    'name[0]',
    'name.call()',
    '(a for a in some())',
    '(1,)',
    '(1, 2, 3)',
])
def test_yield_from_correct_type(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Ensure that `yield from` works with correct types."""
    tree = parse_ast_tree(yield_from_template.format(code))

    visitor = GeneratorKeywordsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
