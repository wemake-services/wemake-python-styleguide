import pytest

from wemake_python_styleguide.violations.best_practices import (
    BaseExceptionViolation,
)
from wemake_python_styleguide.visitors.ast.exceptions import (
    WrongExceptHandlerVisitor,
)

use_base_exception = """
try:
    ...
except BaseException:
    ...
"""

use_except_exception = """
try:
    ...
except Exception:
    ...
"""

use_bare_except = """
try:
    ...
except:
    ...
"""


@pytest.mark.parametrize('code', [
    use_base_exception,
])
def test_use_base_exception(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that `except BaseException:` is restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongExceptHandlerVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BaseExceptionViolation])


@pytest.mark.parametrize('code', [
    use_except_exception,
    use_bare_except,
])
def test_use_exception(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that `except Exception:` and `except:` are allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongExceptHandlerVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
