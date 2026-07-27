import pytest

from wemake_python_styleguide.violations.consistency import (
    SimplifiableMatchViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import (
    SimplifiableMatchVisitor,
)

# Wrong:
simplifiable_match_match = """
match subject:
    case {0}{1}:
        pass
    case _:
        pass
"""

simplifiable_union_match_match = """
match subject:
    case {0} | {1}{2}:
        pass
    case _:
        pass
"""


single_case_sequence = """
match subject:
    case [1, 2, 3]:
        pass
"""

single_case_wildcard = """
match subject:
    case _:
        pass
"""

single_case_literal = """
match subject:
    case '1':
        pass
"""

single_case_guard = """
match subject:
    case x if x > 0:
        pass
"""

# Correct:
complex_match = """
match subject:
    case State.FIRST:
        pass
    case State.SECOND:
        pass
    case _:
        pass
"""

no_wildcard_match = """
match subject:
    case State.FIRST:
        pass
    case State.SECOND:
        pass
"""

guard_match = """
match subject:
    case [x] if x > 0:
        pass
    case _:
        pass
"""

class_with_args_match = """
match subject:
    case SomeClass(x):
        pass
    case _:
        pass
"""

class_with_kwargs_match = """
match subject:
    case SomeClass(name=x):
        pass
    case _:
        pass
"""

sequences_match = """
match subject:
    case [x, *rest]:
        pass
    case _:
        pass
"""

mappings_match = """
match subject:
    case {"key": x}:
        pass
    case _:
        pass
"""

sequence_mapping_template = """
match subject:
    case {pattern}:
        pass
    case _:
        pass
"""

# Wrong sequence:
_SIMPLIFIABLE_PATTERNS = (
    "['a', False, ['b'], {'c': 2, 'x': None}]",
    "{'a': '1', 'b': {'2': [1]}}",
    '[1, 2, 3]',
    "['a', 'b', 'c']",
    '[True, False]',
    "[1, 'a', 2]",
    '[True, 1, False]',
    "[True, 'a', False]",
    "[True, 1, 'a', None]",
)

# Correct sequence:
_NON_SIMPLIFIABLE_PATTERNS = (
    '[x, y, z]',
    '{"key": x}',
    '{"key": [x]}',
    '{"key": 1, **kwargs}',
    "[{'a': x}]",
    "{'a': '1', 'b': {'2': x}}",
    '[1, [x]]',
    '[1, *rest]',
)


@pytest.mark.parametrize('pattern', _SIMPLIFIABLE_PATTERNS)
def test_simplifiable_sequence(
    assert_errors,
    parse_ast_tree,
    default_options,
    pattern,
):
    """Test that patterns with sequence/mapping require simplification."""
    tree = parse_ast_tree(sequence_mapping_template.format(pattern=pattern))
    visitor = SimplifiableMatchVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [SimplifiableMatchViolation])


@pytest.mark.parametrize('pattern', _NON_SIMPLIFIABLE_PATTERNS)
def test_non_simplifiable_patterns(
    assert_errors,
    parse_ast_tree,
    default_options,
    pattern,
):
    """Test that patterns do not require simplification."""
    tree = parse_ast_tree(sequence_mapping_template.format(pattern=pattern))
    visitor = SimplifiableMatchVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        single_case_sequence,
        single_case_literal,
        single_case_guard,
        single_case_wildcard,
    ],
)
def test_simplifiable_single_case_match(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Test that match with only one case."""
    tree = parse_ast_tree(code)
    visitor = SimplifiableMatchVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [SimplifiableMatchViolation])


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
@pytest.mark.parametrize(
    'as_binding',
    ['', ' as x'],
)
def test_simplifiable_single_match(
    code,
    as_binding,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Test that simple single-case match raises a violation."""
    tree = parse_ast_tree(simplifiable_match_match.format(code, as_binding))
    visitor = SimplifiableMatchVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [SimplifiableMatchViolation])


@pytest.mark.parametrize(
    ('left', 'right'),
    [
        ('1', '2'),
        ('True', 'False'),
        ('"a"', '"b"'),
        ('State.OK', 'State.ERROR'),
        ('"first" | "second"', '"third"'),
    ],
)
@pytest.mark.parametrize(
    'as_binding',
    ['', ' as x'],
)
def test_simplifiable_union_match(
    left,
    right,
    as_binding,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Test that union pattern raises violation."""
    tree = parse_ast_tree(
        simplifiable_union_match_match.format(left, right, as_binding),
    )
    visitor = SimplifiableMatchVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [SimplifiableMatchViolation])


@pytest.mark.parametrize(
    'template',
    [
        complex_match,
        no_wildcard_match,
        guard_match,
        class_with_args_match,
        class_with_kwargs_match,
        sequences_match,
        mappings_match,
    ],
)
def test_not_simplifiable_match_templates(
    template,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Test that complex or non-simplifiable matches do not raise violations."""
    tree = parse_ast_tree(template)
    visitor = SimplifiableMatchVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])
