import pytest

from wemake_python_styleguide.violations.refactoring import (
    ImplicitItemsIteratorViolation,
)
from wemake_python_styleguide.visitors.ast.loops import SyncForLoopVisitor

for_loop_template1 = """
for {0} in {1}:
    {2}
"""

for_loop_template2 = """
for {0} in {1}:
    if some:
        {2}
"""

for_loop_template3 = """
for {0} in {1}:
    for other in totally_unrelated:
        {2}
"""


@pytest.mark.parametrize(('target', 'iterable', 'expression'), [
    ('index', 'some', 'some[index]'),
    ('index', 'some', 'print(some[index])'),
    ('index', 'some', 'some[index].call()'),

    ('index', 'some', 'test = some[index]'),
    ('index', 'some', 'test: int = some[index]'),
    ('index', 'some', 'test, value = some[index]'),
    ('index', 'some', 'test = value = some[index]'),
    ('index', 'some', 'some[index] = some[index]'),

    ('index', 'some.attr', 'some.attr[index]'),
    ('index', 'some[0]', 'some[0][index]'),
    ('index', 'call()', 'call()[index]'),
    ('index', 'call(1, 2)', 'call(1, 2)[index]'),
])
@pytest.mark.parametrize('template', [
    for_loop_template1,
    for_loop_template2,
    for_loop_template3,
])
def test_implicit_forloop_items(
    assert_errors,
    parse_ast_tree,
    default_options,
    target,
    iterable,
    expression,
    template,
):
    """Ensures that `.items()` are required."""
    tree = parse_ast_tree(
        template.format(target, iterable, expression),
    )

    visitor = SyncForLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ImplicitItemsIteratorViolation])


@pytest.mark.parametrize(('target', 'iterable', 'expression'), [
    # Correct exmpressions:
    ('index', 'some_other', 'some[index]'),
    ('index_other', 'some', 'print(some[index])'),
    ('index', 'some', 'some.index.call()'),
    ('index', 'call(1, 2)', 'call(1)[index]'),

    # Assignments:
    ('index', 'some', 'some[index] = True'),
    ('index', 'some', 'some[index] += [1, 2, 3]'),
    ('index', 'some', 'some[index] *= 2'),
    ('index', 'some', 'some[index] -= index'),
    ('index', 'some', 'some[index] @= some[other]'),

    # Using `items`:
    ('key, value', 'some.items()', 'some[index]'),
    ('key, value', 'some.items()', 'print(key, value, some)'),
])
@pytest.mark.parametrize('template', [
    for_loop_template1,
    for_loop_template2,
    for_loop_template3,
])
def test_correct_items(
    assert_errors,
    parse_ast_tree,
    default_options,
    target,
    iterable,
    expression,
    template,
):
    """Ensures that wrong types cannot be used as a loop's iter."""
    tree = parse_ast_tree(
        template.format(target, iterable, expression),
    )

    visitor = SyncForLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
