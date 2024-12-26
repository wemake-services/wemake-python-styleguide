import pytest

from wemake_python_styleguide.violations.refactoring import (
    ExtraMatchSubjectSyntax,
)
from wemake_python_styleguide.visitors.ast.pm import MatchSubjectVisitor

template = """
match {0}:
    case SomeClass():
        my_print('first')
"""


@pytest.mark.parametrize(
    'code',
    [
        '[Some()]',
        '[first, second]',
        '{var, other}',
        '{test : result}',
        '{test : "value"}',
        '(one,)',
    ],
)
def test_wrong_usage_of_subjects(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Ensures that extra syntax in subjects are forbidden."""
    tree = parse_ast_tree(template.format(code))

    visitor = MatchSubjectVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ExtraMatchSubjectSyntax])


@pytest.mark.parametrize(
    'code',
    [
        'first',
        'call()',
        'attr.value',
        '(first, second)',
        '(many, items, here)',
        # Will raise another violation:
        '[1, 2]',
        '()',
        '[]',
    ],
)
def test_correct_usage_of_subjects(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Ensures that it is possible to have correct subjects."""
    tree = parse_ast_tree(template.format(code))

    visitor = MatchSubjectVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
