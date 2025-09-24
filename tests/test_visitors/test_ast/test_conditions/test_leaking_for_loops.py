import pytest

from wemake_python_styleguide.violations.best_practices import (
    LeakingForLoopViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import (
    LeakingForLoopVisitor,
)

# Wrong:

module_scope_code = """
for index in range(10):
    ...
"""

class_body_code = """
class ClassWithBody:
    for index in range(10):
        ...
"""

for_with_wrong_del = """
for index in range(10):
    ...
del other
"""

for_unpacking_with_partial_del = """
for a, b in [(1, 2)]:
    ...
del a
"""

separate_classes_false_cleanup = """
class ClassWithFor:
    for index in range(10):
        ...

class ClassWithDel:
    index = ...
    del index
"""

multiple_for_mixed = """
for good in range(5):
    ...
del good

for bad in range(5):
    ...
"""


# Correct

for_with_del_module = """
for index in range(10):
    ...
del index
"""

for_with_del_class = """
class ClassWithDel:
    for index in range(10):
        ...
    del index
"""

for_unpacking_with_del = """
for a, b in [(1, 2)]:
    ...
del a, b
"""

for_with_del_inside_if = """
for i in range(10):
    ...

if True:
    del i
"""


@pytest.mark.parametrize(
    'code',
    [
        module_scope_code,
        class_body_code,
        for_with_wrong_del,
        for_unpacking_with_partial_del,
        separate_classes_false_cleanup,
        multiple_for_mixed,
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
        for_with_del_inside_if,
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
