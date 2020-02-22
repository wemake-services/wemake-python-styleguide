# -*- coding: utf-8 -*-

import pytest

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


@pytest.mark.parametrize('code', [
    right_try_example,
    right_try_example_with_while,
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
