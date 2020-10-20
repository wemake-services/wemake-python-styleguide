import pytest

from wemake_python_styleguide.violations.best_practices import (
    NonTrivialExceptViolation,
)
from wemake_python_styleguide.visitors.ast.exceptions import (
    WrongExceptHandlerVisitor,
)

use_complex_expression = """
try:
    ...
except ValueError or TypeError:
    ...
"""

use_name_expression = """
try:
    ...
except ValueError:
    ...
"""

use_attribute_expression = """
try:
    ...
except exceptions.CustomException:
    ...
"""

use_null_expression = """
try:
    ...
except:
    ...
"""

use_tuple_with_allowed_expression = """
try:
    ...
except (ValueError, TypeError):
    ...
"""

use_tuple_with_forbidden_expressions = """
try:
    ...
except (ValueError, 1 + 2, "sad"):
    ...
"""


@pytest.mark.parametrize('code', [
    use_complex_expression,
    use_tuple_with_forbidden_expressions,
])
def test_use_base_exception(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that `except ValueError or TypeError:` is restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongExceptHandlerVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NonTrivialExceptViolation])


@pytest.mark.parametrize('code', [
    use_name_expression,
    use_attribute_expression,
    use_tuple_with_allowed_expression,
    use_null_expression,
])
def test_use_exception(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that trivial cases are allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongExceptHandlerVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
