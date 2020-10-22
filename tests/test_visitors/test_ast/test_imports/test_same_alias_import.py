import pytest

from wemake_python_styleguide.violations.naming import SameAliasImportViolation
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor

regular_import = 'import os as {0}'
from_import = 'from sys import os as {0}'


@pytest.mark.parametrize('code', [
    regular_import,
    from_import,
])
def test_same_alias_import(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that imports with the same aliases are allowed."""
    same_alias = 'os'
    tree = parse_ast_tree(code.format(same_alias))

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [SameAliasImportViolation])


@pytest.mark.parametrize('code', [
    regular_import,
    from_import,
])
def test_same_alias_import_with_control(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    options,
):
    """Testing that imports with the same aliases are restricted."""
    same_alias = 'os'
    tree = parse_ast_tree(code.format(same_alias))
    custom_options = options(i_control_code=True)

    visitor = WrongImportVisitor(custom_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [SameAliasImportViolation])
    assert_error_text(visitor, same_alias)


@pytest.mark.parametrize('code', [
    regular_import,
    from_import,
])
def test_same_alias_import_without_control(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """Testing that imports with the same aliases are restricted."""
    same_alias = 'os'
    tree = parse_ast_tree(code.format(same_alias))
    custom_options = options(i_control_code=False)

    visitor = WrongImportVisitor(custom_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    regular_import,
    from_import,
])
@pytest.mark.parametrize('to_import', [
    'other',
    'names',
    'sys',
])
def test_other_alias_name(
    assert_errors,
    parse_ast_tree,
    code,
    to_import,
    default_options,
):
    """Testing that imports with other aliases are allowed."""
    tree = parse_ast_tree(code.format(to_import))

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
