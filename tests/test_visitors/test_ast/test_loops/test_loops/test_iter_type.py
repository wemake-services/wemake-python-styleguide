# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    WrongLoopIterTypeViolation,
)
from wemake_python_styleguide.visitors.ast.loops import (
    WrongLoopDefinitionVisitor,
)

for_loop_template = """
def function():
    for index in {0}:
        ...
"""


@pytest.mark.parametrize('code', [
    '[]',
    '[1, 2, 3]',
    '[elem for elem in call()]',
    '{{}}',
    '{"key": value}',
    '{"key": value for value in call()}',
    '{1, 2, 3}',
    '{set_item for set_item in call()}',
])
def test_iter_incorrect_type(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that wrong types cannot be used as a loop's iter."""
    tree = parse_ast_tree(mode(for_loop_template.format(code)))

    visitor = WrongLoopDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongLoopIterTypeViolation])


@pytest.mark.parametrize('code', [
    '()',
    '(1, 2, 3)',
    'name',
    'call()',
    'set()',
    'some.attr',
    'some.method()',
])
def test_iter_correct_type(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that correct types can be used as a loop's iter."""
    tree = parse_ast_tree(mode(for_loop_template.format(code)))

    visitor = WrongLoopDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
