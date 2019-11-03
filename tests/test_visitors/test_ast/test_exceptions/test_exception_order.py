# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    IncorrectExceptOrderViolation,
)
from wemake_python_styleguide.visitors.ast.exceptions import (
    WrongTryExceptVisitor,
)

exception_template = """
try:
    ...
except {0}:
    ...
except {1}:
    ...
"""

custom_exception_template1 = """
try:
    ...
except (MyCustomError1, {0}):
    ...
except (MyCustomError2, {1}):
    ...
"""

custom_exception_template2 = """
try:
    ...
except CustomError:
    ...
except {0}:
    ...
except OtherCustomError:
    ...
except {1}:
    ...
"""


@pytest.mark.parametrize('code', [
    exception_template,
    custom_exception_template1,
    custom_exception_template2,
])
@pytest.mark.parametrize('statements', [
    ('ValueError', 'Exception'),
    ('Exception', 'MyValueError'),
    ('MyCustomException', 'MyValueError'),
])
def test_correct_order_exception(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    statements,
):
    """Testing restrictions are not raised when use correct oder of `except`."""
    tree = parse_ast_tree(code.format(*statements))

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    exception_template,
    custom_exception_template1,
    custom_exception_template2,
])
@pytest.mark.parametrize('statements', [
    ('Exception', 'ValueError'),
    ('Exception', 'KeyError'),
    ('LookupError', 'IndexError'),
    ('BaseException', 'Exception'),
])
def test_wrong_order_exception(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    statements,
):
    """Testing incorrect order of exceptions."""
    tree = parse_ast_tree(code.format(*statements))

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [IncorrectExceptOrderViolation])
