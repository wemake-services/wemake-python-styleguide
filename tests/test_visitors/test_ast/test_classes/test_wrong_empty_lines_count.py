"""Test method contain only allowed empty lines count."""
import pytest

from wemake_python_styleguide.violations.best_practices import (
    WrongEmptyLinesCountVisitorViolation,
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
"""

class_with_allow_method = """
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
    tree = parse_ast_tree(class_with_wrong_method)

    visitor = WrongEmptyLinesCountVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongEmptyLinesCountVisitorViolation])


@pytest.mark.parametrize('input_', [
    class_with_allow_method,
    allow_function,
])
def test_success(
    input_,
    parse_ast_tree,
    default_options,
    assert_errors,
    assert_error_text,
):
    """Testing available cases."""
    tree = parse_ast_tree(class_with_wrong_method)

    visitor = WrongEmptyLinesCountVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongEmptyLinesCountVisitorViolation])
