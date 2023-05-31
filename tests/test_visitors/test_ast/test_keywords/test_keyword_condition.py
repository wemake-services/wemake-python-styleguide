import pytest

from wemake_python_styleguide.violations.best_practices import (
    WrongKeywordConditionViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import (
    ConstantKeywordVisitor,
)

while_template = """
while {0}:
    ...
"""

assert_template = 'assert {0}'
assert_with_message_template = 'assert {0}, "message"'


@pytest.mark.parametrize('code', [
    while_template,
    assert_template,
    assert_with_message_template,
])
@pytest.mark.parametrize('condition', [
    '0',
    '0.0',
    '+0',
    '-1',
    '--2.1',
    '""',
    'b""',
    '[]',
    '()',
    '{}',  # noqa: P103
    '+True',
    'False',
    'None',
    '1',
    '0.1',
    '"0"',
    '[None]',
    '{1, 2, 3}',
    '{name: "0"}',
    '(a for a in some())',
    '[a for a in some()]',
    '{1 for a in some()}',
    '{"a": a for a in some()}',
    'some if x else other',
    '(unique := +0)',
    '(unique := +True)',
])
def test_false_condition_keywords(
    assert_errors,
    parse_ast_tree,
    code,
    condition,
    default_options,
):
    """Testing that false conditions in keywords are restricted."""
    tree = parse_ast_tree(code.format(condition))

    visitor = ConstantKeywordVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongKeywordConditionViolation])


@pytest.mark.parametrize('code', [
    assert_template,
    assert_with_message_template,
])
@pytest.mark.parametrize('condition', [
    'True',
])
def test_false_assert_condition_keywords(
    assert_errors,
    parse_ast_tree,
    code,
    condition,
    default_options,
):
    """Testing that false conditions in keywords are restricted."""
    tree = parse_ast_tree(code.format(condition))

    visitor = ConstantKeywordVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongKeywordConditionViolation])


fixtures = (
    'call()',
    'name',
    '-name',
    'attr.value',
    'attr[index]',
    'method.call()',
    'value in other',
    'value + 1',
    'x > 1',
    'x + 1 > 1 and y < 1',
)


@pytest.mark.parametrize('code', [
    while_template,
])
@pytest.mark.parametrize('condition', [
    *fixtures,
    'x := other()',
])
def test_true_condition_keywords_while(
    assert_errors,
    parse_ast_tree,
    code,
    condition,
    default_options,
):
    """Testing that true conditions in keywords are allowed."""
    tree = parse_ast_tree(code.format(condition))

    visitor = ConstantKeywordVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    assert_template,
    assert_with_message_template,
])
@pytest.mark.parametrize('condition', fixtures)
def test_true_condition_keywords_assert(
    assert_errors,
    parse_ast_tree,
    code,
    condition,
    default_options,
):
    """Testing that true conditions in keywords are allowed."""
    tree = parse_ast_tree(code.format(condition))

    visitor = ConstantKeywordVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    while_template,
])
@pytest.mark.parametrize('condition', [
    'True',
])
def test_true_while_condition_keywords(
    assert_errors,
    parse_ast_tree,
    code,
    condition,
    default_options,
):
    """Testing that true conditions in keywords are allowed."""
    tree = parse_ast_tree(code.format(condition))

    visitor = ConstantKeywordVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
