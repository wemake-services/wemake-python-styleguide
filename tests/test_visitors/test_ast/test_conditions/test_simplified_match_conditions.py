import pytest

from wemake_python_styleguide.violations.consistency import (
    SimplifiableIfMatchViolation,
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

simplifiable_guard_match = """
match subject:
    case x if x > 0:
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


def test_simplifiable_guarded_match(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Test that guarded irrefutable match is simplified."""
    tree = parse_ast_tree(simplifiable_guard_match)
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
        simplifiable_union_match_match.format(left, right, as_binding)
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


# New tests for single-case matches:

# Wrong (single case):
single_case_match = """
match x:
    case {0}:
        do_something()
"""

single_case_with_as_binding_match = """
match x:
    case {0} as y:
        do_something()
"""

# Correct (not single case or has guards):
multi_case_match = """
match x:
    case 1:
        do_something()
    case 2:
        do_something_else()
"""

single_case_with_guard = """
match x:
    case y if y > 0:
        do_something()
"""

wildcard_case = """
match x:
    case _:
        do_something()
"""

pattern_with_complex_structure = """
match x:
    case [a, b]:
        do_something()
"""

pattern_with_class_args = """
match x:
    case SomeClass(a):
        do_something()
"""


@pytest.mark.parametrize(
    'code',
    [
        '1',
        'True',
        'None',
        '"string"',
        'ns.CONST',
        'State.ACCEPTED',
    ],
)
def test_single_case_match(
    code,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Test that single-case matches raise a violation."""
    tree = parse_ast_tree(single_case_match.format(code))
    visitor = SimplifiableMatchVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [SimplifiableIfMatchViolation])


def test_single_case_with_as_binding(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Test that single-case matches with as-binding raise a violation."""
    tree = parse_ast_tree(single_case_with_as_binding_match.format('1'))
    visitor = SimplifiableMatchVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [SimplifiableIfMatchViolation])


@pytest.mark.parametrize(
    'template',
    [
        multi_case_match,
        single_case_with_guard,
        wildcard_case,
        pattern_with_complex_structure,
        pattern_with_class_args,
    ],
)
def test_not_single_case_match(
    template,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Test that non-single-case matches do not raise the single-case violation."""
    tree = parse_ast_tree(template)
    visitor = SimplifiableMatchVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])
