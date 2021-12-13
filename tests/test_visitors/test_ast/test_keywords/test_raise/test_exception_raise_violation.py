import pytest

from wemake_python_styleguide.violations.best_practices import (
    BaseExceptionRaiseViolation,
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

raise_exception_raw = 'raise {0}'

raise_exception_property = """
class CheckAbstractMethods():
    @property
    def check_exception(self):
        raise {0}
"""


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
