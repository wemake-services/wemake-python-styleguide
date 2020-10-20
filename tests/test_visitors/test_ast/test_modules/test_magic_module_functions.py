import pytest

from wemake_python_styleguide.constants import MAGIC_MODULE_NAMES_BLACKLIST
from wemake_python_styleguide.violations.best_practices import (
    BadMagicModuleFunctionViolation,
)
from wemake_python_styleguide.visitors.ast.modules import (
    MagicModuleFunctionsVisitor,
)

module_level_method = """
def {0}(name):
    ...
"""

class_level_method = """
class Example(object):
    def {0}(name):
        ...
"""


@pytest.mark.parametrize('code', [
    module_level_method,
    class_level_method,
])
@pytest.mark.parametrize('function_names', MAGIC_MODULE_NAMES_BLACKLIST)
def test_right_magic_used(
    assert_errors,
    code,
    parse_ast_tree,
    options,
    function_names,
):
    """Testing magic methods with logic is restricted."""
    tree = parse_ast_tree(code.format(function_names))
    option_values = options(i_control_code=False)

    visitor = MagicModuleFunctionsVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    module_level_method,
])
@pytest.mark.parametrize('function_names', MAGIC_MODULE_NAMES_BLACKLIST)
def test_wrong_magic_used(
    assert_errors,
    code,
    parse_ast_tree,
    default_options,
    function_names,
):
    """Testing that some magic methods are restricted."""
    tree = parse_ast_tree(code.format(function_names))

    visitor = MagicModuleFunctionsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BadMagicModuleFunctionViolation])
