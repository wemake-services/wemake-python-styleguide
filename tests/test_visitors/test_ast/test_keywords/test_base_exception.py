# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    BaseExceptionViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import (
    WrongExceptionTypeVisitor,
)

use_baseexception = """
try:
    execute()
except BaseException:
    raise
"""


@pytest.mark.parametrize('code', [
    use_baseexception,
])
def test_use_base_exception(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that `except BaseException:` is restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongExceptionTypeVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BaseExceptionViolation])


def test_exception(
    assert_errors, parse_ast_tree, default_options,
):
    """Testing that `except Exception:` is allowed."""
    tree = parse_ast_tree("""
    try:
        1 / 0
    except Exception:
        raise
    """)

    visitor = WrongExceptionTypeVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


def test_bare_except(
    assert_errors, parse_ast_tree, default_options,
):
    """Testing that bare `except:` is allowed."""
    tree = parse_ast_tree("""
    try:
        1 / 0
    except:
        raise
    """)

    visitor = WrongExceptionTypeVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
