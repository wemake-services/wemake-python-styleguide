"""Test method contain only allowed empty lines count."""
import pytest

from wemake_python_styleguide.violations.best_practices import (
    WrongEmptyLinesCountViolation,
)
from wemake_python_styleguide.visitors.ast.function_empty_lines import (
    WrongEmptyLinesCountVisitor,
)

class_with_wrong_method = """
class WrongClass(object):

    def wrong_method(self):
        foo()

        bar()

        baz()

        lighter()
"""

class_with_valid_method = """
class WrongClass(object):

    def wrong_method(self):
        foo()
        bar()
        baz()
"""

wrong_function = """
def func():
    foo()

    a = 1 + 4

    bar()

    baz()
"""

wrong_function_with_loop = """
def func():
    for x in range(10):

        requests.get(


            'https://github.com/wemake-services/wemake-python-styleguide'
        )
"""

allow_function = """
def func():
    foo()
    if name == 'Moonflower':
        print('Love')

    baz()
"""


allow_function_with_comments = """
def log_customer_info(customer):
    # printing customer name
    print(customer.name)
    # printing customer phone
    print(customer.phone)
    # printing customer company
    print(customer.company)
"""


@pytest.mark.parametrize('input_', [
    class_with_wrong_method,
    wrong_function,
    wrong_function_with_loop,
])
def test_wrong(
    input_,
    default_options,
    assert_errors,
    parse_tokens,
):
    """Testing wrong cases."""
    file_tokens = parse_tokens(input_)

    visitor = WrongEmptyLinesCountVisitor(
        default_options, file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [WrongEmptyLinesCountViolation])


@pytest.mark.parametrize('input_', [
    class_with_valid_method,
    allow_function,
    allow_function_with_comments,
])
def test_success(
    input_,
    parse_tokens,
    default_options,
    assert_errors,
):
    """Testing available cases."""
    file_tokens = parse_tokens(input_)

    visitor = WrongEmptyLinesCountVisitor(
        default_options, file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [])


def test_zero_option(
    parse_tokens,
    default_options,
    assert_errors,
    options,
):
    """Test zero configuration."""
    file_tokens = parse_tokens(allow_function)
    visitor = WrongEmptyLinesCountVisitor(
        options(exps_for_one_empty_line=0), file_tokens=file_tokens,
    )
    visitor.run()
    assert_errors(visitor, [WrongEmptyLinesCountViolation])
