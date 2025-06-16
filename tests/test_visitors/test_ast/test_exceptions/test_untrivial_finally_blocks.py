import pytest

from wemake_python_styleguide.violations.complexity import (
    ComplexFinallyViolation,
)
from wemake_python_styleguide.visitors.ast.exceptions import (
    UntrivialFinallyBlocksVisitor,
)

# Correct:

trivial_logic_example1 = """
try:
    print()
except:
    print()
finally:
    print()
"""

trivial_logic_example2 = """
try:
    print()
except:
    print()
finally:
    print()
    print()
"""

trivial_logic_custom_example1 = """
try:
    print()
except:
    print()
finally:
    print()
    print()
    print()
"""

# Wrong:

untrivial_logic_example1 = """
try:
    print()
except:
    print()
finally:
    print()
    print()
    print()
"""

untrivial_logic_custom_example1 = """
try:
    print()
except:
    print()
finally:
    print()
    print()
    print()
    print()
"""


@pytest.mark.parametrize(
    'code',
    [
        untrivial_logic_example1,
    ],
)
def test_untrivial_try_blocks(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Violations are raised when try blocks are nested."""
    tree = parse_ast_tree(code)

    visitor = UntrivialFinallyBlocksVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ComplexFinallyViolation])


@pytest.mark.parametrize(
    'code',
    [untrivial_logic_example1, untrivial_logic_custom_example1],
)
def test_custom_untrivial_try_blocks(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """Violations are raised when try blocks are nested."""
    tree = parse_ast_tree(code)

    option_values = options(max_lines_in_finally=3)
    visitor = UntrivialFinallyBlocksVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [ComplexFinallyViolation])


@pytest.mark.parametrize(
    'code',
    [trivial_logic_example1, trivial_logic_example2],
)
def test_correct_try_blocks(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Violations are not raised when try block is not nested."""
    tree = parse_ast_tree(code)

    visitor = UntrivialFinallyBlocksVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        trivial_logic_example1,
        trivial_logic_example2,
        trivial_logic_custom_example1,
    ],
)
def test_custom_correct_try_blocks(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """Violations are not raised when try block is not nested."""
    tree = parse_ast_tree(code)

    option_values = options(max_lines_in_finally=3)
    visitor = UntrivialFinallyBlocksVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
