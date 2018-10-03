# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.complexity.jones import (
    JonesComplexityVisitor,
    LineComplexityViolation,
)

line_simple = 'x = 2'
line_with_types = 'x: int = 2'
line_with_comprehension = 'x = [f for f in "abc"]'
line_with_math = 'x = y * 2 + 19 / 9.3'
line_inside_function = """
def some_function():
    return 2 + 1
"""

line_inside_async_function = """
async def some_function():
    return 2 + 1
"""

line_inside_class = """
class SomeClass():
    field = 13 / 2
"""

class_with_function = """
class First:
    def second():
        return 2 + 1
"""

class_with_async_function = """
class First:
    async def second():
        return 2 + 1
"""

class_with_usual_and_async_function = """
class First:
    async def second():
        return 2 + 1

    def third():
        return 2 + 2
"""

function_declaration = 'def some_function(): ...'
async_function_declaration = 'async def some_function(): ...'
class_declaration = 'class SomeClass(object): ...'
empty_module = ''


@pytest.mark.parametrize('code', [
    line_simple,
    line_with_types,
    line_with_comprehension,
    line_with_math,
    line_inside_function,
    line_inside_async_function,
    line_inside_class,
    function_declaration,
    async_function_declaration,
    class_declaration,
    empty_module,
    class_with_function,
    class_with_async_function,
    class_with_usual_and_async_function,
])
def test_regular_nodes(assert_errors, parse_ast_tree, code, default_options):
    """Testing that regular nodes do not raise violations."""
    tree = parse_ast_tree(code)

    visitor = JonesComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    line_simple,
    line_inside_function,
    line_inside_async_function,
    line_inside_class,
])
def test_complex_lines(assert_errors, parse_ast_tree, code, options):
    """Testing that complex lines do raise violations."""
    tree = parse_ast_tree(code)

    option_values = options(max_line_complexity=1)
    visitor = JonesComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [LineComplexityViolation])


def test_same_complexity(parse_ast_tree, default_options):
    """Ensures that complexity is counted correctly."""
    tree_without_types = parse_ast_tree(line_simple)
    tree_with_types = parse_ast_tree(line_with_types)

    simple_visitor = JonesComplexityVisitor(
        default_options, tree=tree_without_types,
    )
    typed_visitor = JonesComplexityVisitor(
        default_options, tree=tree_with_types,
    )

    simple_visitor.run()
    typed_visitor.run()

    assert len(simple_visitor._lines) == 1
    assert len(simple_visitor._lines[1]) == 3
    assert len(simple_visitor._lines[1]) == len(typed_visitor._lines[1])


@pytest.mark.parametrize('code, complexity', [
    (line_with_comprehension, 6),
    (line_with_math, 9),
])
def test_exact_complexity(parse_ast_tree, default_options, code, complexity):
    """Ensures that complexity is counted correctly."""
    tree = parse_ast_tree(code)

    visitor = JonesComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert len(visitor._lines) == 1
    assert len(visitor._lines[1]) == complexity


@pytest.mark.parametrize('code, number_of_lines', [
    (line_inside_function, 1),
    (line_inside_async_function, 1),
    (class_with_async_function, 1),
    (class_with_function, 1),
    (class_with_usual_and_async_function, 2),
])
def test_that_some_nodes_are_ignored(
    parse_ast_tree, default_options, code, assert_errors, number_of_lines,
):
    """Ensures that complexity is counted correctly."""
    tree = parse_ast_tree(code)

    visitor = JonesComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert len(visitor._lines) == number_of_lines
