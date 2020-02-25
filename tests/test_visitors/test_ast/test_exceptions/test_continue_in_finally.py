# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.compat.constants import PY38
from wemake_python_styleguide.violations.best_practices import (
    ContinueInFinallyBlockViolation,
)
from wemake_python_styleguide.visitors.ast.exceptions import (
    WrongTryExceptVisitor,
)

right_try_example = """
for element in range(10):
    try:
        ...
    except:
        ...
    finally:
        ...
"""

right_try_example_with_while = """
while first_element < second_element:
    try:
        ...
    except:
        ...
    finally:
        ...
"""

right_continue_example_in_for = """
def some():
    for elem in range(10):
        if elem > 5:
            continue
"""

right_continue_example_in_while = """
def some():
    while a < b:
        if a == 5:
            continue
"""

wrong_try_example = """
for element in range(10):
    try:
        ...
    except:
        ...
    finally:
        continue
"""

wrong_try_example_with_while = """
while first_element < second_element:
    try:
        ...
    except:
        ...
    finally:
        continue
"""


@pytest.mark.skipif(
    not PY38,
    reason='continue in finally works only since python3.8',
)
@pytest.mark.parametrize('code', [
    wrong_try_example,
    wrong_try_example_with_while,
])
def test_wrong_finally(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Violations are raised when finally without except in try block."""
    tree = parse_ast_tree(code)

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ContinueInFinallyBlockViolation])


@pytest.mark.skipif(
    not PY38,
    reason='continue in finally works only since python3.8',
)
@pytest.mark.parametrize('code', [
    right_try_example,
    right_try_example_with_while,
    right_continue_example_in_for,
    right_continue_example_in_while,
])
def test_correct_finally(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Violations are not raised when finally with except in try block."""
    tree = parse_ast_tree(code)

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
