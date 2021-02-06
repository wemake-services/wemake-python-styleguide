import pytest

from wemake_python_styleguide.violations.best_practices import (
    ProtectedModuleMemberViolation,
    ProtectedModuleViolation,
)
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor

import_public = 'import public'
import_protected = 'import _protected'
import_from_protected = 'from _protected import something'
import_from_protected_path = 'from path._protected import something'
import_protected_from = 'from some.path import _protected'
import_from_public = 'from public import something'
import_from_public_path = 'from public.path import something'
import_protected_as_alias = 'from some.path import _protected as not_protected'


@pytest.mark.parametrize('code', [
    import_public,
    import_from_public,
    import_from_public_path,
])
def test_correct_import(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that correct imports are allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    import_protected,
    import_from_protected,
    import_from_protected_path,
])
def test_incorrect_modules_import(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that imports from protected modules are restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ProtectedModuleViolation])
    assert_error_text(visitor, '_protected')


@pytest.mark.parametrize('code', [
    import_protected_from,
    import_protected_as_alias,
])
def test_incorrect_module_members_import(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that importing of protected objects is restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ProtectedModuleMemberViolation])
    assert_error_text(visitor, '_protected')
