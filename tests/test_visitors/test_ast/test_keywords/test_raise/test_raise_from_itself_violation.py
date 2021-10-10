import pytest

from wemake_python_styleguide.violations.best_practices import (
    RaiseFromItselfViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import WrongRaiseVisitor

raise_from_itself_outside_try = """
e = Exception('Some Exception')
raise e from e
"""

raise_from_itself_inside_try = """
def raise_from_itself():
    try:
        print('test')
    except Exeception as ex:
        raise ex from ex
"""


@pytest.mark.parametrize('code', [
    raise_from_itself_outside_try,
    raise_from_itself_inside_try,
])
def test_raise_from_itself(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that are not allowed to raise an exception from itself."""
    tree = parse_ast_tree(code)

    visitor = WrongRaiseVisitor(default_options, tree)
    visitor.run()

    assert_errors(visitor, [RaiseFromItselfViolation])


raise_from_other_exception_outside_try = """
first_exception = Exception('First Exception')
second_exception = Exception('Second Exception')
raise second_exception from first_exception
"""

raise_from_other_exception_inside_try = """
try:
    raise TypeError('Type Error')
except TypeError as ex:
    raise NameError('New Exception') from ex
"""


@pytest.mark.parametrize('code', [
    raise_from_other_exception_outside_try,
    raise_from_other_exception_inside_try,
])
def test_raise_from_other_exception(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that are allowed to raise an exception from other exception."""
    tree = parse_ast_tree(code)

    visitor = WrongRaiseVisitor(default_options, tree)
    visitor.run()

    assert_errors(visitor, [])
