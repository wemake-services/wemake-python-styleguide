import pytest

from wemake_python_styleguide.violations.best_practices import (
    LeakingForLoopViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import (
    LeakingForLoopVisitor,
)

module_scope_code = 'for index in range(10):\n    index = index + 1'
class_body_code = (
    'class ClassWithBody:\n'
    '    for index in range(10):\n'
    '        index = index + 1'
)

for_with_del_module = f'{module_scope_code}\ndel index'
for_with_del_class = (
    'class ClassWithDel:\n'
    '    for index in range(10):\n'
    '        index = index + 1\n'
    '    del index'
)

for_with_wrong_del = f'{module_scope_code}\ndel other'

for_unpacking_with_del = 'for a, b in [(1, 2)]:\n    print(a, b)\ndel a, b'

for_unpacking_with_partial_del = 'for a, b in [(1, 2)]:\n    print(a, b)\ndel a'

multiple_for_mixed = (
    'for good in range(5):\n'
    '    print(good)\n'
    'del good\n'
    '\n'
    'for bad in range(5):\n'
    '    print(bad)'
)


@pytest.mark.parametrize(
    'code',
    [
        module_scope_code,
        class_body_code,
        for_with_wrong_del,
        for_unpacking_with_partial_del,
    ],
    ids=[
        'module_scope',
        'class_body',
        'wrong_del',
        'partial_unpacking_del',
    ],
)
def test_leaking_for_loop_violation(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Ensure leaking for loops without proper cleanup raise a violation."""
    tree = parse_ast_tree(code)

    visitor = LeakingForLoopVisitor(default_options, tree)
    visitor.run()

    assert_errors(visitor, [LeakingForLoopViolation])


@pytest.mark.parametrize(
    'code',
    [
        for_with_del_module,
        for_with_del_class,
        for_unpacking_with_del,
    ],
    ids=[
        'module_with_del',
        'class_with_del',
        'unpacking_with_del',
    ],
)
def test_for_loop_with_del_no_violation(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Ensure `for` loops with proper `del` do not raise a violation."""
    tree = parse_ast_tree(code)

    visitor = LeakingForLoopVisitor(default_options, tree)
    visitor.run()

    assert_errors(visitor, [])


def test_multiple_for_loops_mixed(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Tests reports only the leaking loop when multiple are present."""
    tree = parse_ast_tree(multiple_for_mixed)

    visitor = LeakingForLoopVisitor(default_options, tree)
    visitor.run()

    assert_errors(visitor, [LeakingForLoopViolation])
