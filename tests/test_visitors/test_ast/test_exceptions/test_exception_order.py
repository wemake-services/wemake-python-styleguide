import pytest

from wemake_python_styleguide.compat.constants import PY311
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

exception_star_template = """
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


@pytest.mark.parametrize(
    'code',
    [
        exception_template,
        pytest.param(
            exception_star_template,
            marks=pytest.mark.skipif(
                not PY311,
                reason='ExceptionGroup was added in python 3.11',
            ),
        ),
        custom_exception_template1,
        custom_exception_template2,
    ],
)
@pytest.mark.parametrize(
    'statements',
    [
        ('ValueError', 'Exception'),
        ('Exception', 'MyValueError'),
        ('MyCustomException', 'MyValueError'),
    ],
)
def test_correct_order_exception(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    statements,
):
    """Violations are not raised when using the correct order of `except`."""
    tree = parse_ast_tree(code.format(*statements))

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        exception_template,
        pytest.param(
            exception_star_template,
            marks=pytest.mark.skipif(
                not PY311,
                reason='ExceptionGroup was added in python 3.11',
            ),
        ),
        custom_exception_template1,
        custom_exception_template2,
    ],
)
@pytest.mark.parametrize(
    'statements',
    [
        ('Exception', 'ValueError'),
        ('Exception', 'KeyError'),
        ('LookupError', 'IndexError'),
        ('BaseException', 'Exception'),
    ],
)
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
