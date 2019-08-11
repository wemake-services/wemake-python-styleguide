# -*- coding: utf-8 -*-

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
    '""',
    '[]',
    '()',
    '{}',  # noqa: P103
    'False',
    'None',
])
def test_false_condition_keywords(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    condition,
    default_options,
):
    """Testing that false coniditions in keywords are restricted."""
    tree = parse_ast_tree(code.format(condition))

    visitor = ConstantKeywordVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongKeywordConditionViolation])
    assert_error_text(visitor, condition)


@pytest.mark.parametrize('code', [
    while_template,
    assert_template,
    assert_with_message_template,
])
@pytest.mark.parametrize('condition', [
    '1',
    '0.1',
    '"0"',
    '[None]',
    '{1, 2, 3}',
    '{name: "0"}',
    'True',

    'call()',
    'name',
    'attr.value',
    'attr[index]',
    'method.call()',
    'value in other',
    'value + 1',
    'set()',
])
def test_true_condition_keywords(
    assert_errors,
    parse_ast_tree,
    code,
    condition,
    default_options,
):
    """Testing that true coniditions in keywords are allowed."""
    tree = parse_ast_tree(code.format(condition))

    visitor = ConstantKeywordVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
