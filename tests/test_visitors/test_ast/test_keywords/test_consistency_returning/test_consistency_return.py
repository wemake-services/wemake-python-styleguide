import pytest

from wemake_python_styleguide.violations.consistency import (
    InconsistentReturnViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import (
    ConsistentReturningVisitor,
)

# Correct:

correct_example1 = """
def function():
    ...
"""

correct_example2 = """
def function():
    return 'value'
"""

correct_example3 = """
def function():
    if some:
        return 1
    return None
"""

correct_example4 = """
def function():
    if some:
        return

    if other:
        return
    print()
"""

correct_example5 = """
def function():
    if some:
        return 1
    return False
"""

correct_example6 = """
def function():
    return True
"""

correct_example7 = """
def function():
    if some:
        return 1

    if other:
        return 2
    print()
    return 3
"""

correct_example8 = '''
def function():
    """some"""
'''

correct_example9 = """
def function():
    def factory():
        return 1
    return None  # single `return None` statement if this context
"""

# Wrong:

wrong_example1 = """
def function():
    return
"""

wrong_example2 = """
def function():
    print(1)
    return None
"""

wrong_example3 = """
def function():
    if some:
        return

    if other:
        return
    print()
    return
"""

wrong_example4 = """
def function():
    def decorator():
        return
    return decorator
"""

wrong_example5 = """
def function():
    return None
"""

wrong_example6 = '''
def function():
    """some"""
    return None
'''

wrong_example7 = '''
def function():
    """some"""
    return
'''

double_wrong_return1 = """
def function():
    if some:
        return
    return None
"""

double_wrong_return2 = """
def function():
    if some:
        return None

    return
"""


@pytest.mark.parametrize('code', [
    wrong_example1,
    wrong_example2,
    wrong_example3,
    wrong_example4,
    wrong_example5,
    wrong_example6,
    wrong_example7,
])
def test_wrong_return_statement(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing incorrect `return` statements."""
    tree = parse_ast_tree(mode(code))

    visitor = ConsistentReturningVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [InconsistentReturnViolation])


@pytest.mark.parametrize('code', [
    double_wrong_return1,
    double_wrong_return2,
])
def test_douple_wrong_return_statement(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing double incorrect `return` statements."""
    tree = parse_ast_tree(mode(code))

    visitor = ConsistentReturningVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        InconsistentReturnViolation,
        InconsistentReturnViolation,
    ])


@pytest.mark.parametrize('code', [
    correct_example1,
    correct_example2,
    correct_example3,
    correct_example4,
    correct_example5,
    correct_example6,
    correct_example7,
    correct_example8,
    correct_example9,
])
def test_correct_return_statements(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing correct `return` statements."""
    tree = parse_ast_tree(mode(code))

    visitor = ConsistentReturningVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
