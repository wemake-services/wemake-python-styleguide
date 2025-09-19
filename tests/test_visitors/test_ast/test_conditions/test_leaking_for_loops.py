import pytest

from wemake_python_styleguide.violations.best_practices import (
    LeakingForLoopViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import (
    LeakingForLoopVisitor,
)


@pytest.mark.parametrize(
    'code',
    [
        'for index in range(10):\n    index = index + 1',
        (
            'class ClassWithBody:\n'
            '    for index in range(10):\n'
            '        index = index + 1'
        ),
    ],
    ids=['module_scope', 'class_body'],
)
def test_leaking_for_loop_violation(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Ensure leaking for loops in class/module scopes raise a violation."""
    tree = parse_ast_tree(code)

    visitor = LeakingForLoopVisitor(default_options, tree)
    visitor.run()

    assert_errors(visitor, [LeakingForLoopViolation])
