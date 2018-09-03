# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.wrong_import import (
    SameAliasImportViolation,
    WrongImportVisitor,
)

regular_import = """
import os as {0}
"""

from_import = """
from sys import os as {0}
"""


@pytest.mark.parametrize('code', [
    regular_import,
    from_import,
])
def test_same_alias_import(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that imports with the same aliases are restricted."""
    tree = parse_ast_tree(code.format('os'))

    visiter = WrongImportVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [SameAliasImportViolation])


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
    assert_errors, parse_ast_tree, code, to_import, default_options,
):
    """Testing that imports with other aliases are allowed."""
    tree = parse_ast_tree(code.format(to_import))

    visiter = WrongImportVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [])
