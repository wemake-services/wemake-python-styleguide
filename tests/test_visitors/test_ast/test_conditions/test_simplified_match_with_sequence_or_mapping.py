import pytest

from wemake_python_styleguide.violations.consistency import (
    SimplifiableMatchWithSequenceOrMappingViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import (
    SimplifiableMatchWithSequenceOrMappingVisitor,
)

# Wrong: Simple sequence patterns
simple_list_match = """
match data:
    case [1, 2]:
        handle_pair()
    case _:
        ignore()
"""

simple_nested_list_match = """
match data:
    case [[1, 2], [3, 4]]:
        handle_nested()
    case _:
        ignore()
"""

simple_tuple_match = """
match data:
    case (1, "a"):
        handle_tuple()
    case _:
        ignore()
"""

simple_dict_match = """
match data:
    case {"key": "value"}:
        handle_dict()
    case _:
        ignore()
"""

simple_nested_dict_match = """
match data:
    case {"outer": {"inner": 42}}:
        handle_nested_dict()
    case _:
        ignore()
"""

mixed_list_dict_match = """
match data:
    case [{"key": "value"}, 42]:
        handle_mixed()
    case _:
        ignore()
"""

# Correct: Complex patterns that should not be simplified
complex_with_binding = """
match data:
    case [x, y]:
        handle_with_binding(x, y)
    case _:
        ignore()
"""

with_star_pattern = """
match data:
    case [first, *rest]:
        handle_with_rest(first, rest)
    case _:
        ignore()
"""

with_rest_name = """
match data:
    case {"key": value, **rest}:
        handle_with_rest(value, rest)
    case _:
        ignore()
"""

with_guard = """
match data:
    case [1, 2] if condition > 0:
        handle_guarded()
    case _:
        ignore()
"""

complex_match = """
match data:
    case SomeClass(x):
        handle_class()
    case _:
        ignore()
"""

no_wildcard = """
match data:
    case [1, 2]:
        handle_first()
    case [3, 4]:
        handle_second()
"""

more_than_two_cases = """
match data:
    case [1, 2]:
        handle_first()
    case [3, 4]:
        handle_second()
    case _:
        handle_default()
"""


@pytest.mark.parametrize(
    'code',
    [
        simple_list_match,
        simple_nested_list_match,
        simple_tuple_match,
        simple_dict_match,
        simple_nested_dict_match,
        mixed_list_dict_match,
    ],
)
def test_simplifiable_sequence_or_mapping_match(
    code,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Test that simple sequence and mapping matches raise a violation."""
    tree = parse_ast_tree(code)
    visitor = SimplifiableMatchWithSequenceOrMappingVisitor(
        default_options, tree=tree
    )
    visitor.run()
    assert_errors(visitor, [SimplifiableMatchWithSequenceOrMappingViolation])


@pytest.mark.parametrize(
    'template',
    [
        complex_with_binding,
        with_star_pattern,
        with_rest_name,
        with_guard,
        complex_match,
        no_wildcard,
        more_than_two_cases,
    ],
)
def test_not_simplifiable_sequence_or_mapping_match(
    template,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Test that complex or non-simplifiable matches do not raise violations."""
    tree = parse_ast_tree(template)
    visitor = SimplifiableMatchWithSequenceOrMappingVisitor(
        default_options, tree=tree
    )
    visitor.run()
    assert_errors(visitor, [])
