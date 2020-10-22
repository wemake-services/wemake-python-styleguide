import pytest

from wemake_python_styleguide.constants import FUTURE_IMPORTS_WHITELIST
from wemake_python_styleguide.violations.best_practices import (
    FutureImportViolation,
)
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor

future_import = 'from __future__ import {0}'

future_import_alias = 'from __future__ import {0} as some_alias'


@pytest.mark.parametrize('code', [
    future_import,
    future_import_alias,
])
@pytest.mark.parametrize('to_import', [
    'print_function',
    'with_statement',
    'unicode_literals',
])
def test_wrong_future_import(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    to_import,
    default_options,
):
    """Testing that future imports are restricted."""
    tree = parse_ast_tree(code.format(to_import))

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [FutureImportViolation])
    assert_error_text(visitor, to_import)


def test_wrong_multiple_future_import(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing that multiple future imports are restricted."""
    tree = parse_ast_tree(
        'from __future__ import print_function, unicode_literals',
    )

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [FutureImportViolation, FutureImportViolation])


@pytest.mark.parametrize('code', [
    future_import,
    future_import_alias,
])
@pytest.mark.parametrize('to_import', FUTURE_IMPORTS_WHITELIST)
def test_correct_future_import(
    assert_errors, parse_ast_tree, code, to_import, default_options,
):
    """Testing that some future imports are not restricted."""
    tree = parse_ast_tree(code.format(to_import), do_compile=False)

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
