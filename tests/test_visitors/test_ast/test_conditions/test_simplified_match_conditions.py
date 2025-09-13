import pytest

from wemake_python_styleguide.violations.consistency import (
    SimplifiableMatchViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import (
    SimplifiableMatchVisitor,
)

# Wrong:
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

simplifiable_with_const_as_binding_template = """
    match subject:
        case State.REJECTED as status:
            pass
        case _:
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
    case x if x > 0:
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
    tree = parse_ast_tree(simplifiable_with_const_as_binding_template)
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
