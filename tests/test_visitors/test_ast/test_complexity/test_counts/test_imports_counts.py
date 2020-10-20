import pytest

from wemake_python_styleguide.violations.complexity import (
    TooManyImportedModuleMembersViolation,
    TooManyImportedNamesViolation,
    TooManyImportsViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.imports import (
    ImportMembersVisitor,
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

import_from_multiple_names = 'from module import name0, name1, name2'


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


@pytest.mark.parametrize('code', [
    module_with_from_imports,
    import_from_multiple_names,
])
def test_import_from_correct_number_of_names(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    options,
):
    """Violation not raised when max value not reached."""
    tree = parse_ast_tree(code)

    option_values = options(max_import_from_members=3)
    visitor = ImportMembersVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    import_from_multiple_names,
])
def test_import_from_too_many_members(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    options,
):
    """Testing that violations are raised when reaching max value."""
    tree = parse_ast_tree(code)

    option_values = options(max_import_from_members=2)
    visitor = ImportMembersVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyImportedModuleMembersViolation])
    assert_error_text(visitor, '3', option_values.max_import_from_members)
