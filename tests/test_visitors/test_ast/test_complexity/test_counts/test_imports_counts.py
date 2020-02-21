# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.complexity import (
    TooManyImportedNamesViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.counts import (
    ImportMembersVisitor,
    TooManyImportsViolation,
)

module_import = ''
module_with_regular_imports = """
import sys
import os
"""

module_with_from_imports = """
from os import path
from sys import version
"""


@pytest.mark.parametrize('code', [
    module_import,
    module_with_regular_imports,
    module_with_from_imports,
])
def test_module_import_counts_normal(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that imports in a module work well."""
    tree = parse_ast_tree(code)

    visitor = ImportMembersVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    module_with_regular_imports,
    module_with_from_imports,
])
def test_module_import_counts_violation(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    options,
):
    """Testing that violations are raised when reaching max value."""
    tree = parse_ast_tree(code)

    option_values = options(max_imports=1)
    visitor = ImportMembersVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyImportsViolation])
    assert_error_text(visitor, '2', option_values.max_imports)


@pytest.mark.parametrize('code', [
    module_with_regular_imports,
    module_with_from_imports,
])
def test_module_imported_names_counts_violation(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    options,
):
    """Testing that violations are raised when reaching max value."""
    tree = parse_ast_tree(code)

    option_values = options(max_imported_names=1)
    visitor = ImportMembersVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyImportedNamesViolation])
    assert_error_text(visitor, '2', option_values.max_imported_names)
