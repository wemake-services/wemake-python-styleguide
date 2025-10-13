import pytest

from wemake_python_styleguide.violations.consistency import (
    SimplifiableSequenceOrMappingMatchViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import (
    SimplifiableSequenceOrMappingMatchVisitor,
)

# Wrong:
simple_sequence = """
match data:
    case {0}:
        pass
    case _:
        pass
"""

simple_mapping = """
match data:
    case {0}:
        pass
    case _:
        pass
"""


# Correct:
binding_sequence = """
match data:
    case [x]:
        pass
    case _:
        pass
"""

starred_sequence = """
match data:
    case [1, *rest]:
        pass
    case _:
        pass
"""

mapping_with_binding = """
match data:
    case {"x": value}:
        pass
    case _:
        pass
"""

with_guard = """
match data:
    case [1, 2] if flag:
        pass
    case _:
        pass
"""

as_binding = """
match data:
    case [1, 2] as x:
        pass
    case _:
        pass
"""

complex_sequence = """
match data:
    case [1, [3, 4]]:
        pass
    case _:
        pass
"""

complex_name = """
match data:
    case [some_var]:
        pass
    case _:
        pass
"""

three_cases = """
match data:
    case [1]:
        pass
    case [2]:
        pass
    case _:
        pass
"""


@pytest.mark.parametrize(
    'code',
    [
        [1, 'a'],
        [2, 3],
        ['x', 'y'],
    ],
)
def test_simplifiable_sequence_match_violation(
    code, assert_errors, parse_ast_tree, default_options
):
    """Test that simple sequence match raises a violation."""
    tree = parse_ast_tree(simple_sequence.format(code))
    visitor = SimplifiableSequenceOrMappingMatchVisitor(
        default_options, tree=tree
    )
    visitor.run()
    assert_errors(visitor, [SimplifiableSequenceOrMappingMatchViolation])


@pytest.mark.parametrize(
    'code',
    [
        {'a': 1},
        {'x': 2, 'y': 3},
        {4: 'b'},
    ],
)
def test_simplifiable_mapping_match_violation(
    code, assert_errors, parse_ast_tree, default_options
):
    """Test that simple mapping match raises a violation."""
    tree = parse_ast_tree(simple_mapping.format(code))
    visitor = SimplifiableSequenceOrMappingMatchVisitor(
        default_options, tree=tree
    )
    visitor.run()
    assert_errors(visitor, [SimplifiableSequenceOrMappingMatchViolation])


@pytest.mark.parametrize(
    'code',
    [
        binding_sequence,
        starred_sequence,
        mapping_with_binding,
        with_guard,
        as_binding,
        complex_sequence,
        complex_name,
        three_cases,
    ],
)
def test_not_simplifiable_structural_match(
    code, assert_errors, parse_ast_tree, default_options
):
    """Test that complex or non-simplifiable matches do not raise violations."""
    tree = parse_ast_tree(code)
    visitor = SimplifiableSequenceOrMappingMatchVisitor(
        default_options, tree=tree
    )
    visitor.run()
    assert_errors(visitor, [])
