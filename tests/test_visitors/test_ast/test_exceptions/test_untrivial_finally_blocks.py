import pytest

from wemake_python_styleguide.violations.complexity import (
    ComplexFinallyViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.complex_finally import (
    ComplexFinallyBlocksVisitor,
)

# Correct examples:

trivial_logic_example1 = """
try:
    my_print('error')
except:
    my_print('error')
finally:
    my_print('error')
"""

trivial_logic_example2 = """
try:
    my_print('error')
except:
    my_print('error')
finally:
    my_print('error')
    my_print('error')
"""

trivial_logic_example3 = """
try:
    my_print('error')
finally:
    my_print('error')
"""

trivial_logic_example4 = """
try:
    my_print('error')
finally:
    my_print('error')
    my_print('error')
"""

# Wrong examples:

untrivial_logic_default_example1 = """
try:
    my_print('error')
finally:
    my_print('error')
    my_print('error')
    my_print('error')
"""

untrivial_logic_default_example2 = """
try:
    my_print('error')
except:
    my_print('error')
finally:
    my_print('error')
    my_print('error')
    my_print('error')
"""

untrivial_logic_custom_example1 = """
try:
    my_print('error')
except:
    my_print('error')
finally:
    my_print('error')
    my_print('error')
    my_print('error')
    my_print('error')
"""

untrivial_logic_custom_example2 = """
try:
    my_print('error')
finally:
    my_print('error')
    my_print('error')
    my_print('error')
    my_print('error')
"""


@pytest.mark.parametrize(
    'code',
    [untrivial_logic_default_example1, untrivial_logic_default_example2],
)
def test_untrivial_try_blocks(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Violations are raised when finally blocks exceed default line limit."""
    tree = parse_ast_tree(code)

    visitor = ComplexFinallyBlocksVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ComplexFinallyViolation])


@pytest.mark.parametrize(
    'code',
    [untrivial_logic_custom_example1, untrivial_logic_custom_example2],
)
def test_custom_untrivial_try_blocks(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """Violations are raised when finally blocks exceed custom line limit."""
    tree = parse_ast_tree(code)

    option_values = options(max_lines_in_finally=2)
    visitor = ComplexFinallyBlocksVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [ComplexFinallyViolation])


@pytest.mark.parametrize(
    'code',
    [
        trivial_logic_example1,
        trivial_logic_example2,
        trivial_logic_example3,
        trivial_logic_example4,
    ],
)
def test_correct_try_blocks(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """No violations for finally blocks within default line limit."""
    tree = parse_ast_tree(code)

    visitor = ComplexFinallyBlocksVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        trivial_logic_example1,
        trivial_logic_example2,
        trivial_logic_example3,
        trivial_logic_example4,
        untrivial_logic_default_example1,
        untrivial_logic_default_example2,
    ],
)
def test_custom_correct_try_blocks(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """No violations for finally blocks within custom line limit."""
    tree = parse_ast_tree(code)

    option_values = options(max_lines_in_finally=2)
    visitor = ComplexFinallyBlocksVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
