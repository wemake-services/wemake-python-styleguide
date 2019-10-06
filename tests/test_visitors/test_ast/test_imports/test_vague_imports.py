# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    VagueImportViolation,
)
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor

import_template = 'from mod import {0}'

blacklisted_method_names = [
    'dump',
    'dumps',
    'load',
    'loads',
    'parse',
    'safe_dump',
    'safe_dump_all',
    'load_all',
    'dump_all',
    'safe_load_all',
    'safe_dump_all',
]


@pytest.mark.parametrize(
    'method_name',
    blacklisted_method_names + ['a', 'from_something', 'to_something'],
)
def test_special_cases_vague_import(
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
