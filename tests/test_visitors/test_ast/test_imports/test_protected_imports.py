# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    ImportProtectedModuleViolation,
)
from wemake_python_styleguide.violations.consistency import (
    DottedRawImportViolation,
)
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor

# Incorrect imports:
protected_import = 'import _protected'
protected_from_import = 'from public import _protected'
multiple_protected_import_from = 'from public import another, _protected'
protected_import_from = 'from _protected import something'
nested_protected_import_from = 'from something._protected import another'

# Correct imports:
regular_import = 'import public'
regular_from_import = 'from something import public'
regular_nested_import = 'from something.public import another'


@pytest.mark.parametrize('code', [
    protected_import,
    protected_from_import,
    multiple_protected_import_from,
    protected_import_from,
    nested_protected_import_from,
])
def test_protected_import(assert_errors, parse_ast_tree, code, default_options):
    """Testing import protected modules are restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ImportProtectedModuleViolation])


def test_nested_protected_import(
    assert_errors, parse_ast_tree, default_options,
):
    """Testing nested import protected modules are restricted."""
    tree = parse_ast_tree('import something._protected')

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        DottedRawImportViolation,
        ImportProtectedModuleViolation,
    ])


@pytest.mark.parametrize('code', [
    regular_import,
    regular_from_import,
    regular_nested_import,
])
def test_regular_imports(assert_errors, parse_ast_tree, code, default_options):
    """Testing that regular imports are allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
