import pytest

from wemake_python_styleguide.violations.consistency import (
    SingleCaseMatchViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import (
    SimplifiableMatchVisitor,
)

# Wrong: single case without guard
single_case_match = """
match subject:
    case {0}:
        pass
"""

# Wrong: single case with as binding
single_case_with_as = """
match subject:
    case {0} as x:
        pass
"""

# Correct: single case with guard (should not raise)
single_case_with_guard = """
match subject:
    case {0} if check():
        pass
"""

# Correct: multiple cases (should not raise)
multi_case_match = """
match subject:
    case 1:
        pass
    case 2:
        pass
"""

# Correct: single case with wildcard (should not raise)
single_wildcard_match = """
match subject:
    case _:
        pass
"""

# Correct: single case irrefutable binding (should not raise)
single_irrefutable_match = """
match subject:
    case x:
        pass
"""


@pytest.mark.parametrize(
    'code',
    [
        '1',
        'True',
        'None',
        '"string"',
        'ns.CONST',
        'State.REJECTED',
    ],
)
def test_single_case_match_violation(
    code,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Test that single-case match raises a violation."""
    tree = parse_ast_tree(single_case_match.format(code))
    visitor = SimplifiableMatchVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [SingleCaseMatchViolation])


@pytest.mark.parametrize(
    'code',
    [
        '1',
        'True',
        'None',
        '"string"',
    ],
)
def test_single_case_with_as_violation(
    code,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Test that single-case match with as binding raises a violation."""
    tree = parse_ast_tree(single_case_with_as.format(code))
    visitor = SimplifiableMatchVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [SingleCaseMatchViolation])


@pytest.mark.parametrize(
    'code',
    [
        '1',
        'True',
        'None',
        '"string"',
    ],
)
def test_single_case_with_guard_no_violation(
    code,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Test that single-case match with guard does not raise."""
    tree = parse_ast_tree(single_case_with_guard.format(code))
    visitor = SimplifiableMatchVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'template',
    [
        multi_case_match,
        single_wildcard_match,
        single_irrefutable_match,
    ],
)
def test_no_violation_templates(
    template,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Test that non-violating patterns do not raise."""
    tree = parse_ast_tree(template)
    visitor = SimplifiableMatchVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])
