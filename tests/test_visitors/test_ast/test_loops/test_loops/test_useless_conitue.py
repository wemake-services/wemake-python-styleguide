import pytest

from wemake_python_styleguide.violations.consistency import (
    UselessContinueViolation,
)
from wemake_python_styleguide.visitors.ast.loops import WrongLoopVisitor

# Correct:

correct_for_loop = """
def wrapper():
    for number in [123]:
        if number < 0:
            continue
        print(number)
"""

correct_while_loop = """
while True:
    if number < 0:
        continue

    if number == 0:
        continue

    print(number)
"""

# Wrong:

wrong_for_loop = """
def wrapper():
    for number in [123]:
        continue
"""

wrong_nested_for_loop = """
def wrapper():
    for number in [123]:
        if number < 0:
            continue
"""

wrong_while_loop = """
while True:
    continue
"""

wrong_nested_while_loop = """
while True:
    if number == 0:
        continue
"""


@pytest.mark.parametrize('code', [
    wrong_for_loop,
    wrong_nested_for_loop,
    wrong_while_loop,
    wrong_nested_while_loop,
])
def test_wrong_continue_in_loop(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Violations are raised when `continue` is the last statement."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessContinueViolation])


@pytest.mark.parametrize('code', [
    correct_for_loop,
    correct_while_loop,
])
def test_correct_continue_usage(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Violations are not raised when `continue` is not the last statement."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
