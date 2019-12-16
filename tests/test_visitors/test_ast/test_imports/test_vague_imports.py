# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide import constants
from wemake_python_styleguide.violations.consistency import (
    VagueImportViolation,
)
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor

import_template = 'from mod import {0}'
alias_import_template = 'from mod import something as {0}'


@pytest.mark.parametrize('code', [
    alias_import_template,
    import_template,
])
@pytest.mark.parametrize('import_name', [
    *constants.VAGUE_IMPORTS_BLACKLIST,
    'Q',
    'F_',
    '__a',
    '__s__',
    'from_thing',
    'to_thing',
])
def test_vague_method_name_import(
    assert_errors,
    parse_ast_tree,
    code,
    import_name,
    default_options,
):
    """Testing that imports with the same aliases are restricted."""
    tree = parse_ast_tree(code.format(import_name))

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [VagueImportViolation])


@pytest.mark.parametrize('code', [
    alias_import_template,
    import_template,
])
@pytest.mark.parametrize('import_name', [
    '_',
    'Long',
    '__some__',
    'S_A',
    'some_from_other',
    'first_to_second',
])
def test_regular_import(
    assert_errors,
    parse_ast_tree,
    code,
    import_name,
    default_options,
):
    """Testing that regular imports are ok."""
    tree = parse_ast_tree(code.format(import_name))

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
