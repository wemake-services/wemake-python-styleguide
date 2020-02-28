import pytest

from wemake_python_styleguide.violations.best_practices import (
    RaiseNotImplementedViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import WrongRaiseVisitor

raise_not_implemented_method = """
class CheckAbstractMethods():
    def check_not_implemented(self):
        raise {0}
"""

raise_not_implemented_function = """
def check_not_implemented_without_call():
    raise {0}
"""

raise_not_implemented_property = """
class CheckAbstractMethods():
    @property
    def check_not_implemented(self):
        raise {0}
"""

raise_not_implemented_raw = 'raise {0}'


@pytest.mark.parametrize('code', [
    raise_not_implemented_method,
    raise_not_implemented_function,
    raise_not_implemented_raw,
    raise_not_implemented_property,
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
    raise_not_implemented_method,
    raise_not_implemented_function,
    raise_not_implemented_raw,
    raise_not_implemented_property,
])
@pytest.mark.parametrize('exception', [
    'NotImplementedError',
    'NotImplementedError()',
])
def test_raise_not_implemented_error(
    assert_errors,
    parse_ast_tree,
    code,
    exception,
    default_options,
    mode,
):
    """Testing that `raise NotImplementedError` is allowed."""
    tree = parse_ast_tree(mode(code.format(exception)))

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


def test_bare_raise(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing that bare `raise` is allowed."""
    tree = parse_ast_tree("""
    try:
        1 / 0
    except Exception:
        raise
    """)

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
