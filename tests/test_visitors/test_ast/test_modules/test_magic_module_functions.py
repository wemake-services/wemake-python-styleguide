# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.constants import MAGIC_MODULE_NAMES_BLACKLIST
from wemake_python_styleguide.violations.best_practices import (
    BadMagicModuleFunctionViolation,
)
from wemake_python_styleguide.visitors.ast.modules import (
    MagicModuleFunctionsVisitor,
)

regular_function = """
def {0}(name):
    ...
"""


@pytest.mark.parametrize('function_names', MAGIC_MODULE_NAMES_BLACKLIST)
def test_wrong_magic_used(
    assert_errors,
    parse_ast_tree,
    default_options,
    function_names,
):
    """Testing that some magic methods are restricted."""
    tree = parse_ast_tree(regular_function.format(function_names))

    visitor = MagicModuleFunctionsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BadMagicModuleFunctionViolation])
