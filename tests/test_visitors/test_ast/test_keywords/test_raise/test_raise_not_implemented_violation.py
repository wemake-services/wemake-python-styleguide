import pytest

from wemake_python_styleguide.violations.best_practices import (
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
