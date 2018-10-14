# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    BaseExceptionViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import (
    WrongExceptionTypeVisitor,
)

use_base_exception = """
try:
    execute()
except BaseException:
    raise
"""

use_except_exception = """
try:
    1 / 0
except Exception:
    raise
"""

use_try_except = """
try:
    1 / 0
except:
    raise
"""


@pytest.mark.parametrize('code', [
    use_base_exception,
])
def test_use_base_exception(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that `except BaseException:` is restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongExceptionTypeVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BaseExceptionViolation])


@pytest.mark.parametrize('code', [
    use_except_exception,
])
def test_exception(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that `except Exception:` is allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongExceptionTypeVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    use_try_except,
])
def test_bare_except(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that bare `except:` is allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongExceptionTypeVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
