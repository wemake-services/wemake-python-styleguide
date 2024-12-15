import pytest

from wemake_python_styleguide.compat.constants import PY311
from wemake_python_styleguide.violations.complexity import (
    TooManyExceptExceptionsViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.counts import (
    TryExceptVisitor,
)

except_four_exceptions1 = """
try:
    ...
except (TypeError, ValueError, LookupError, KeyboardInterrupt):
    ...
"""

except_four_exceptions2 = """
try:
    ...
except (TypeError, ValueError, LookupError, KeyboardInterrupt):
    ...
except:
    ...
"""

except_four_exceptions3 = """
try:
    ...
except KeyError as exc:
    ...
except (TypeError, ValueError, LookupError, KeyboardInterrupt):
    ...
"""

except_four_exceptions_star = """
try:
    ...
except* (TypeError, ValueError, LookupError, KeyboardInterrupt):
    ...
"""

except_three_exceptions1 = """
try:
    ...
except (TypeError, ValueError, LookupError):
    ...
"""

except_three_exceptions2 = """
try:
    ...
except (IndexError, ):
    ...
except (TypeError, ValueError, LookupError) as exc:
    ...
"""

except_three_exceptions_star = """
try:
    ...
except* (TypeError, ValueError, LookupError) as exc:
    ...
"""


@pytest.mark.parametrize(
    'code',
    [
        except_four_exceptions1,
        except_four_exceptions2,
        except_four_exceptions3,
        pytest.param(
            except_four_exceptions_star,
            marks=pytest.mark.skipif(
                not PY311,
                reason='ExceptionGroup was added in python 3.11',
            ),
        ),
        except_three_exceptions1,
        except_three_exceptions2,
        pytest.param(
            except_three_exceptions_star,
            marks=pytest.mark.skipif(
                not PY311,
                reason='ExceptionGroup was added in python 3.11',
            ),
        ),
    ],
)
def test_exceptions_modified_count(
    assert_errors,
    parse_ast_tree,
    options,
    code,
):
    """Testing that exceptions counted correctly with option."""
    tree = parse_ast_tree(code)

    option_values = options(max_except_exceptions=5)
    visitor = TryExceptVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        except_four_exceptions1,
        except_four_exceptions2,
        except_four_exceptions3,
        pytest.param(
            except_four_exceptions_star,
            marks=pytest.mark.skipif(
                not PY311,
                reason='ExceptionGroup was added in python 3.11',
            ),
        ),
    ],
)
def test_exceptions_wrong_count(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that exceptions are counted correctly."""
    tree = parse_ast_tree(code)

    visitor = TryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyExceptExceptionsViolation])
    assert_error_text(visitor, '4', default_options.max_except_exceptions)


@pytest.mark.parametrize(
    'code',
    [
        except_three_exceptions1,
        except_three_exceptions2,
        pytest.param(
            except_three_exceptions_star,
            marks=pytest.mark.skipif(
                not PY311,
                reason='ExceptionGroup was added in python 3.11',
            ),
        ),
    ],
)
def test_exceptions_correct_count(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that exceptions are counted correctly."""
    tree = parse_ast_tree(code)

    visitor = TryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
