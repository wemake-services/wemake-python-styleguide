# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    UselessExceptCaseViolation,
)
from wemake_python_styleguide.visitors.ast.exceptions import (
    WrongExceptHandlerVisitor,
)

right_empty_bare_except = """
try:
    ...
except:
    ...
"""

right_logging_except = """
try:
    ...
except Exception:
    sentry.log()
    raise
"""

right_reraise_logging_except = """
try:
    ...
except Exception as ex:
    sentry.log()
    raise ex
"""

right_raise_different_except = """
try:
    ...
except Exception as ex:
    raise APIException()
"""

right_raise_different_var_except = """
try:
    ...
except (TypeError, IndexError) as ex:
    raise other_exception
"""

# Wrong:

wrong_reraise_except = """
try:
    ...
except Exception as ex:
    raise ex
"""

wrong_raise_except = """
try:
    ...
except Exception as ex:
    raise
"""

wrong_bare_raise_except = """
try:
    ...
except Exception:
    raise
"""


@pytest.mark.parametrize('code', [
    wrong_reraise_except,
    wrong_raise_except,
    wrong_bare_raise_except,
])
def test_useless_except_case(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Violations are raised when using wrong except case."""
    tree = parse_ast_tree(code)

    visitor = WrongExceptHandlerVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessExceptCaseViolation])


@pytest.mark.parametrize('code', [
    right_empty_bare_except,
    right_logging_except,
    right_reraise_logging_except,
    right_raise_different_except,
    right_raise_different_var_except,
])
def test_correct_except_case(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Violations are not raised when using correct except case."""
    tree = parse_ast_tree(code)

    visitor = WrongExceptHandlerVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
