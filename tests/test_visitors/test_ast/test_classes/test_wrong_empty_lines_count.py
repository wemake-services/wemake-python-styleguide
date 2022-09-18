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

    baz()
"""

wrong_function_with_loop = """
def func():
    for x in range(10):

        requests.get('https://github.com/wemake-services/wemake-python-styleguide')
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
    parse_ast_tree,
    default_options,
    assert_errors,
    assert_error_text,
):
    """Testing wrong cases."""
    tree = parse_ast_tree(input_)

    visitor = WrongEmptyLinesCountVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongEmptyLinesCountViolation])


@pytest.mark.parametrize('input_', [
    class_with_valid_method,
    allow_function,
    allow_function_with_comments,
])
def test_success(
    input_,
    parse_ast_tree,
    default_options,
    assert_errors,
    assert_error_text,
):
    """Testing available cases."""
    tree = parse_ast_tree(input_)

    visitor = WrongEmptyLinesCountVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongEmptyLinesCountViolation])
