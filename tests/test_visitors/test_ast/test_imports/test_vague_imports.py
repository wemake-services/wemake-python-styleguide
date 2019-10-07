# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide import constants
from wemake_python_styleguide.violations.consistency import (
    VagueImportViolation,
)
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor

import_template = 'from mod import {0}'

alias_import_template = 'from mod import something as {0}'


@pytest.mark.parametrize(
    'method_name',
    list(constants.VAGUE_IMPORTS_BLACKLIST) + ['a', 'from_thing', 'to_thing'],
)
def test_vague_method_name_import(
    assert_errors,
    parse_ast_tree,
    method_name,
    default_options,
):
    """Testing that imports with the same aliases are restricted."""
    tree = parse_ast_tree(import_template.format(method_name))

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [VagueImportViolation])


@pytest.mark.parametrize(
    'alias',
    list(constants.VAGUE_IMPORTS_BLACKLIST) + ['a', 'from_a', 'to_a'],
)
def test_vague_alias_import(
    assert_errors,
    parse_ast_tree,
    alias,
    default_options,
):
    """Testing that imports with the same aliases are restricted."""
    tree = parse_ast_tree(alias_import_template.format(alias))

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [VagueImportViolation])
