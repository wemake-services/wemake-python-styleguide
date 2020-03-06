import pytest

from wemake_python_styleguide.violations.consistency import (
    LocalFolderImportViolation,
)
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor

# Wrong:
same_level_relative_import = 'from . import some_thing'
same_level_relative_import_sibling = 'from .some_thing import MyClass'
parent_level_relative_import = 'from .. import some_thing'
parent_level_relative_import_sibling = 'from ..some_thing import MyClass'
grand_level_relative_import_sibling = 'from ...some_thing import MyClass'

# Correct:
regular_import = 'import os'
regular_from_import = 'from os import path'
regular_nested_import = 'from some.package import Thing'


@pytest.mark.parametrize('code', [
    same_level_relative_import,
    same_level_relative_import_sibling,
    parent_level_relative_import,
    parent_level_relative_import_sibling,
    grand_level_relative_import_sibling,
])
def test_local_folder_import(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that relative to local folder imports are restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [LocalFolderImportViolation])


@pytest.mark.parametrize('code', [
    regular_import,
    regular_from_import,
    regular_nested_import,
])
def test_regular_import(assert_errors, parse_ast_tree, code, default_options):
    """Testing that regular imports are allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
