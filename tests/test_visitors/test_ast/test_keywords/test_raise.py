import pytest

from wemake_python_styleguide.violations.best_practices import (
    BareRaiseViolation,
    BaseExceptionRaiseViolation,
    RaiseFromItselfViolation,
    RaiseNotImplementedViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import WrongRaiseVisitor

raise_exception_method = """
class CheckAbstractMethods():
    def check_exception(self):
        raise {0}
"""

raise_exception_function = """
def check_exception_without_call():
    raise {0}
"""

raise_exception_property = """
class CheckAbstractMethods():
    @property
    def check_exception(self):
        raise {0}
"""

raise_exception_raw = 'raise {0}'


@pytest.mark.parametrize('code', [
    raise_exception_method,
    raise_exception_function,
    raise_exception_raw,
    raise_exception_property,
])
@pytest.mark.parametrize('exception', [
    'NotImplemented',
    'NotImplemented()',
])
def test_raise_not_implemented(
    assert_errors,
    parse_ast_tree,
    code,
    exception,
    default_options,
    mode,
):
    """Testing that `raise NotImplemented` is restricted."""
    tree = parse_ast_tree(mode(code.format(exception)))

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [RaiseNotImplementedViolation])


@pytest.mark.parametrize('code', [
    raise_exception_method,
    raise_exception_function,
    raise_exception_raw,
    raise_exception_property,
])
@pytest.mark.parametrize('exception', [
    'BaseException',
    'BaseException()',
    'Exception',
    'Exception()',
])
def test_raise_base_exception(
    assert_errors,
    parse_ast_tree,
    code,
    exception,
    default_options,
    mode,
):
    """Testing `raise BaseException` and `raise Exception` are restricted."""
    tree = parse_ast_tree(mode(code.format(exception)))

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BaseExceptionRaiseViolation])


@pytest.mark.parametrize('code', [
    raise_exception_method,
    raise_exception_function,
    raise_exception_raw,
    raise_exception_property,
])
@pytest.mark.parametrize('exception', [
    'NotImplementedError',
    'NotImplementedError()',
    'UserDefinedError',
    'UserDefinedError()',
])
def test_raise_good_errors(
    assert_errors,
    parse_ast_tree,
    code,
    exception,
    default_options,
    mode,
):
    """Testing that good `raise` usages are allowed."""
    tree = parse_ast_tree(mode(code.format(exception)))

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


def test_bare_raise_wrong_visitor(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing that bare `raise` is allowed."""
    code = """
    try:
        1 / 0
    except Exception:
        raise
    """
    tree = parse_ast_tree(code)

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


bare_raise_except_function = """
def bare_raise_with_except():
    try:
        print('test')
    except:
        raise
"""

bare_raise_if_function = """
def bare_raise_with_if():
    try:
        print('test')
    except:
        if 1 == 1:
            raise
"""


def test_bare_raise(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing bare raise without except block."""
    code = """
    def bare_raise():
        raise
    """
    tree = parse_ast_tree(code)

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BareRaiseViolation])


@pytest.mark.parametrize('code', [
    bare_raise_except_function,
    bare_raise_if_function,
])
def test_bare_raise_except(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that bare `raise` is only allowed in except blocks."""
    tree = parse_ast_tree(code)

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


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
