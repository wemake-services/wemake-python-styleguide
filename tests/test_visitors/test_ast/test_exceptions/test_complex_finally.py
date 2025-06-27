import pytest

from wemake_python_styleguide.violations.complexity import (
    ComplexFinallyViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.complex_finally import (
    ComplexFinallyBlocksVisitor,
)

# Correct:

no_finally = """
try:
    ...
except:
    ...
"""

correct_example1 = """
try:
    ...
except:
    ...
finally:
    ...
"""

correct_example2 = """
try:
    ...
finally:
    ...
"""

correct_example3 = """
try:
    ...
except:
    ...
finally:
    ...  # 2 lines
    ...
"""

correct_example4 = """
try:
    ...
finally:
    if ...:  # 2 lines
        ...
"""

# Wrong:

wrong_example1 = """
try:
    ...
finally:
    if ...:  # 4 lines
        ...
    else:
        ...
"""

wrong_example2 = """
try:
    ...
except:
    ...
finally:
    if ...:  # 3 lines
        ...
        ...
    ...  # +1 line
"""

wrong_example3 = """
try:
    ...
except:
    ...
else:
    ...
finally:
    try:  # 4 lines
        ...
    except:
        ...
"""

wrong_example4 = """
try:
    ...
finally:
    ...  # 4 lines
    ...
    ...
    ...
"""


@pytest.mark.parametrize(
    'code',
    [
        wrong_example1,
        wrong_example2,
        wrong_example3,
        wrong_example4,
    ],
)
def test_untrivial_try_blocks(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
):
    """Violations are raised when finally blocks exceed default line limit."""
    tree = parse_ast_tree(code)

    visitor = ComplexFinallyBlocksVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ComplexFinallyViolation])
    assert_error_text(visitor, '4', baseline=2)


@pytest.mark.parametrize(
    'code',
    [
        no_finally,
        correct_example1,
        correct_example2,
        correct_example3,
        correct_example4,
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
        no_finally,
        correct_example1,
        correct_example2,
        correct_example3,
        correct_example4,
        wrong_example1,
        wrong_example2,
        wrong_example3,
        wrong_example4,
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

    option_values = options(max_lines_in_finally=5)
    visitor = ComplexFinallyBlocksVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        correct_example3,
        correct_example4,
        wrong_example1,
        wrong_example2,
        wrong_example3,
        wrong_example4,
    ],
)
def test_custom_low_max_lines_in_finally(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """Setting `max_lines_in_finally` to 1 will report many usages."""
    tree = parse_ast_tree(code)

    option_values = options(max_lines_in_finally=1)
    visitor = ComplexFinallyBlocksVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [ComplexFinallyViolation])
