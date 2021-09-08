import pytest

from wemake_python_styleguide.violations.consistency import (
    InconsistentYieldViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import (
    ConsistentReturningVisitor,
)

# Correct:

correct_example1 = """
def function():
    yield
"""

correct_example2 = """
def function():
    yield
    yield
"""

correct_example3 = """
def function():
    yield 1
    yield 2
"""

correct_example4 = """
def function():
    yield 1
    yield None
"""

correct_example5 = """
def function():
    if some:
        yield 1
    yield None
"""

correct_example6 = """
def function():
    yield 1
"""

correct_example7 = """
def function():
    if some:
        yield None
    if other:
        yield None
    yield 1
"""

correct_example8 = """
def function():
    if some:
        yield
    if other:
        yield
    yield
"""

# Wrong:

wrong_example1 = """
def function():
    if some:
        yield
    yield None
"""

wrong_example2 = """
def function():
    if some:
        yield None
    yield
"""

wrong_example3 = """
def function():
    yield None
    yield
"""

wrong_example4 = """
def function():
    if some:
        yield None
    if other:
        yield None
    yield None
"""


@pytest.mark.parametrize('code', [
    wrong_example1,
    wrong_example2,
    wrong_example3,
    wrong_example4,
])
def test_wrong_yield_statement(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing incorrect `yield` statements."""
    tree = parse_ast_tree(mode(code))

    visitor = ConsistentReturningVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [InconsistentYieldViolation])


@pytest.mark.parametrize('code', [
    correct_example1,
    correct_example2,
    correct_example3,
    correct_example4,
    correct_example5,
    correct_example6,
    correct_example7,
    correct_example8,
])
def test_correct_yield_statements(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing correct `yield` statements."""
    tree = parse_ast_tree(mode(code))

    visitor = ConsistentReturningVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
