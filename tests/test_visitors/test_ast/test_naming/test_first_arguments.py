import pytest

from wemake_python_styleguide.constants import SPECIAL_ARGUMENT_NAMES_WHITELIST
from wemake_python_styleguide.visitors.ast.naming.validation import (
    WrongNameVisitor,
)

lambda_first_argument = 'lambda {0}: ...'
function_first_argument = 'def function({0}): ...'

method_first_argument = """
class Test(object):
    def method({0}): ...
"""

classmethod_first_argument = """
class Test(object):
    @classmethod
    def method({0}): ...
"""

meta_first_argument = """
class Test(type):
    def __new__({0}): ...
"""


@pytest.mark.parametrize('argument', SPECIAL_ARGUMENT_NAMES_WHITELIST)
@pytest.mark.parametrize('code', [
    function_first_argument,
    method_first_argument,
    classmethod_first_argument,
    meta_first_argument,
])
def test_correct_first_arguments(
    assert_errors,
    parse_ast_tree,
    argument,
    code,
    default_options,
    mode,
):
    """Testing that first arguments are allowed."""
    tree = parse_ast_tree(mode(code.format(argument)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
