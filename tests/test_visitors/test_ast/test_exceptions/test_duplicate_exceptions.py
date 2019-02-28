# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    DuplicateExceptionViolation,
)
from wemake_python_styleguide.visitors.ast.exceptions import (
    WrongTryExceptVisitor,
)

# Correct:

correct_bare_except = """
try:
    ...
except:
    ...
"""

correct_simple_except = """
try:
    ...
except Exception:
    ...
"""

correct_simple_except_with_name = """
try:
    ...
except Exception as ex:
    ...
"""

correct_two_exceptions = """
try:
    ...
except (IndexError, ValueError):
    ...
"""

correct_two_exceptions_with_names = """
try:
    ...
except (IndexError, ValueError) as ex:
    ...
"""

correct_two_excepts = """
try:
    ...
except ValueError:
    ...
except IndexError:
    ...
"""

correct_two_excepts_with_names = """
try:
    ...
except ValueError as ex:
    ...
except IndexError as ex:
    ...
"""

correct_two_complex_excepts = """
try:
    ...
except ValueError as ex:
    ...
except (IndexError, model.DoesNotExist) as ex:
    ...
"""

# Wrong:

wrong_simple = """
try:
    ...
except ValueError as ex:
    ...
except ValueError:
    ...
"""

wrong_single_tuple = """
try:
    ...
except (some.ValueError, some.ValueError) as ex:
    ...
"""

wrong_different_tuples = """
try:
    ...
except (exc['type'], ValueError) as ex:
    ...
except (exc['type'], IndexError):
    ...
"""


@pytest.mark.parametrize('code', [
    correct_bare_except,
    correct_simple_except,
    correct_simple_except_with_name,
    correct_two_exceptions,
    correct_two_exceptions_with_names,
    correct_two_excepts,
    correct_two_excepts_with_names,
    correct_two_complex_excepts,
])
def test_correct_exceptions(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Violations without duplicates."""
    tree = parse_ast_tree(code)

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_simple,
    wrong_single_tuple,
    wrong_different_tuples,
])
def test_duplicate_exceptions(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
):
    """Duplicate exception classes should raise a violation."""
    tree = parse_ast_tree(code)

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [DuplicateExceptionViolation])
