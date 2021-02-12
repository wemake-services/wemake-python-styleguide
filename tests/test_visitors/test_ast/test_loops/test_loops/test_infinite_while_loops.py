import pytest

from wemake_python_styleguide.violations.best_practices import (
    InfiniteWhileLoopViolation,
)
from wemake_python_styleguide.visitors.ast.loops import WrongLoopVisitor

template_simple = """
while True:
    {0}
"""

template_nested_while1 = """
while True:
    while other:
        {0}
    {0}
"""

template_nested_while2 = """
while other:
    while +1:
        {0}
    {0}
"""

template_nested_if = """
while True:
    if some:
        {0}
"""

template_function = """
def wrapper():
    while True:
        {0}
"""

template_other = """
while other:
    {0}
"""

# Double:

template_double_while = """
while True:
    while 'inf':
        {0}
    {1}
"""

# Correct

correct_while1 = """
while 1:
    try:
       ...
    except:
        ...
"""

correct_while2 = """
while other:
    while [1, 2, 3]:
        try:
            ...
        except:
            ...
"""


correct_while3 = """
def wrapper():
    while True:
        try:
            ...
        except:
            ...
"""

correct_while4 = """
while other:
    ...
"""

correct_while5 = """
while 1 + 1:
    try:
        ...
    except:
        ...
    finally:
        ...
"""

correct_while6 = """
while 0:
    ...
"""

# Do raise:

wrong_while1 = """
while other:
    try:
        ...
    except:
        ...

    while True:
        ...
"""

wrong_while2 = """
while True:
    try:
        ...
    finally:
        ...
"""


@pytest.mark.parametrize('template', [
    template_simple,
    template_nested_while1,
    template_nested_while2,
    template_nested_if,
    template_function,
    template_other,
])
@pytest.mark.parametrize('keyword', [
    'break',
    'raise Some',
    'raise Some()',
    'raise',
])
def test_correct_while_loops_with_statements(
    assert_errors,
    parse_ast_tree,
    keyword,
    template,
    default_options,
):
    """Testing while loops with correct code."""
    tree = parse_ast_tree(template.format(keyword))

    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    correct_while1,
    correct_while2,
    correct_while3,
    correct_while4,
    correct_while5,
    correct_while6,
])
def test_correct_while_loops_with_try(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing while loops with correct code."""
    tree = parse_ast_tree(code)

    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    template_function,
])
@pytest.mark.parametrize('keyword', [
    'return',
    'return some',
])
def test_correct_while_loops_function(
    assert_errors,
    parse_ast_tree,
    keyword,
    template,
    default_options,
    mode,
):
    """Testing while loops with ``return`` statements."""
    tree = parse_ast_tree(mode(template.format(keyword)))

    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    template_simple,
    template_nested_while1,
    template_nested_while2,
    template_nested_if,
    template_function,
])
@pytest.mark.parametrize('keyword', [
    'print(some)',
    'attr.method()',
    'a = 1',
])
def test_wrong_while_loops(
    assert_errors,
    parse_ast_tree,
    keyword,
    template,
    default_options,
):
    """Testing while loops with wrong code."""
    tree = parse_ast_tree(template.format(keyword))

    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [InfiniteWhileLoopViolation])


@pytest.mark.parametrize('code', [
    wrong_while1,
    wrong_while2,
])
def test_wrong_while_loops_with_try(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing while loops with correct code."""
    tree = parse_ast_tree(code)

    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [InfiniteWhileLoopViolation])


@pytest.mark.parametrize('template', [
    template_double_while,
])
@pytest.mark.parametrize('keyword', [
    'break',
    'raise ValueError',
])
def test_double_while_correct_loops(
    assert_errors,
    parse_ast_tree,
    keyword,
    template,
    default_options,
):
    """Testing while loops with wrong code."""
    tree = parse_ast_tree(template.format(keyword, keyword))

    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    template_double_while,
])
@pytest.mark.parametrize(('keyword1', 'keyword2'), [
    ('print()', 'break'),
    ('break', 'other.attr = 1'),
])
def test_double_while_wrong_loops(
    assert_errors,
    parse_ast_tree,
    keyword1,
    keyword2,
    template,
    default_options,
):
    """Testing while loops with wrong code."""
    tree = parse_ast_tree(template.format(keyword1, keyword2))

    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [InfiniteWhileLoopViolation])
