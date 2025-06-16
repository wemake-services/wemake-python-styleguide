import pytest

from wemake_python_styleguide.violations.complexity import (
    UntrivialLogicInFinallyViolation,
)
from wemake_python_styleguide.visitors.ast.exceptions import (
    UntrivialFinallyBlocksVisitor,
)

# Correct:

trivial_logic_example1 = """
try:
    ...
except:
    ...
finally:
    ...
"""

trivial_logic_example2 = """
try:
    ...
except:
    ...
finally:
    ...
    ...
"""

# Wrong:

untrivial_logic_example1 = """
try:
    ...
except:
    ...
finally:
    ...
    ...
    ...
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

    assert_errors(visitor, [UntrivialLogicInFinallyViolation])


@pytest.mark.parametrize(
    'code',
    [
        trivial_logic_example1,
        trivial_logic_example2
    ],
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
