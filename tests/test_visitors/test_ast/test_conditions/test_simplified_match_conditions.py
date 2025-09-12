import pytest

from wemake_python_styleguide.violations.consistency import (
    SimplifiableMatchViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import (
    SimplifiableMatchVisitor,
)

simplifiable_match_template = """
match subject:
    case {0}:
        pass
    case _:
        pass
"""

simplifiable_union_match_template = """
match subject:
    case {0} | {1}:
        pass
    case _:
        pass
"""

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

sequence_match = """
match subject:
    case [1, 2]:
        pass
    case _:
        pass
"""

mapping_match = """
match subject:
    case {"status": "ok"}:
        pass
    case _:
        pass
"""

class_match = """
match subject:
    case SomeClass():
        pass
    case _:
        pass
"""

guard_match = """
match subject:
    case x if x > 0:
        pass
    case _:
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
def test_simplifiable_single_match(
    code: str,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Test that simple single-case match raises a violation."""
    tree = parse_ast_tree(simplifiable_match_template.format(code))
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
def test_simplifiable_union_match(
    left: str,
    right: str,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Test that union pattern raises violation."""
    tree = parse_ast_tree(simplifiable_union_match_template.format(left, right))
    visitor = SimplifiableMatchVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [SimplifiableMatchViolation])


def test_simplifiable_with_const_as_binding(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Test that `case CONST as name:` is still simplifiable."""
    code = """
    match subject:
        case State.REJECTED as status:
            pass
        case _:
            pass
    """
    tree = parse_ast_tree(code)
    visitor = SimplifiableMatchVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [SimplifiableMatchViolation])


@pytest.mark.parametrize(
    'template',
    [
        complex_match,
        no_wildcard_match,
        sequence_match,
        mapping_match,
        class_match,
        guard_match,
    ],
)
def test_not_simplifiable_match_templates(
    template: str,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Test that complex or non-simplifiable matches do not raise violations."""
    tree = parse_ast_tree(template)
    visitor = SimplifiableMatchVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])
