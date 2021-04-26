import pytest

from wemake_python_styleguide.violations.best_practices import (
    BaseExceptionRaiseViolation,
    RaiseNotImplementedViolation,
)
from wemake_python_styleguide.violations.refactoring import BareRaiseViolation
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

raise_exception_with_except = """
def check_exception_without_call():
    try:
        x = 1
    except Exception:
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


@pytest.mark.parametrize(('raise_statement', 'bare_option'), [
    ("ValueError('1')", True),
    ("ValueError('1')", False),
    ('', True),
])
def test_bare_raise_correct(
    assert_errors,
    parse_ast_tree,
    default_options,
    raise_statement,
    bare_option,
):
    """Testing correct instances of `raise SomeException()` and bare `raise`."""
    code = None
    if bare_option:
        code = raise_exception_with_except.format(raise_statement)
    else:
        code = raise_exception_function.format(raise_statement)

    tree = parse_ast_tree(code)

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


def test_bare_raise_no_except(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing that bare `raise` is not allowed without an except block."""
    code = raise_exception_raw.format('')
    tree = parse_ast_tree(code)

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BareRaiseViolation])
