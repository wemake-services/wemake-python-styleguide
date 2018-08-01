# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.wrong_import import (
    DottedRawImportViolation,
    WrongImportVisitor,
)

regular_import = """
import {0}
"""

regular_import_with_alias = """
import {0} as alias
"""

from_import = """
from {0} import some
"""

from_import_with_alias = """
from {0} import some as alias
"""


@pytest.mark.parametrize('code', [
    regular_import,
    regular_import_with_alias,
])
@pytest.mark.parametrize('to_import', [
    'dotted.path'
    'nested.dotted.path',
])
def test_wrong_dotted_import(assert_errors, parse_ast_tree, code, to_import):
    """Testing that dotted raw imports are restricted."""
    tree = parse_ast_tree(code.format(to_import))

    visiter = WrongImportVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [DottedRawImportViolation])


@pytest.mark.parametrize('code', [
    regular_import,
    regular_import_with_alias,
])
@pytest.mark.parametrize('to_import', [
    'os',
    'sys',
])
def test_correct_flat_import(assert_errors, parse_ast_tree, code, to_import):
    """Testing that flat raw imports are allowed."""
    tree = parse_ast_tree(code.format(to_import))

    visiter = WrongImportVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [])


@pytest.mark.parametrize('code', [
    from_import,
    from_import_with_alias,
])
@pytest.mark.parametrize('to_import', [
    'regular',
    'dotted.path'
    'nested.dotted.path',
])
def test_regular_from_import(assert_errors, parse_ast_tree, code, to_import):
    """Testing that dotted `from` imports are allowed."""
    tree = parse_ast_tree(code.format(to_import))

    visiter = WrongImportVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [])
