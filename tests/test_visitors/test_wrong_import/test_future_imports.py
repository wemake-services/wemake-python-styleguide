# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.constants import FUTURE_IMPORTS_WHITELIST
from wemake_python_styleguide.visitors.wrong_import import (
    FutureImportViolation,
    WrongImportVisitor,
)

future_import = """
from __future__ import {0}
"""

future_import_alias = """
from __future__ import {0} as some_alias
"""


@pytest.mark.parametrize('code', [
    future_import,
    future_import_alias,
])
@pytest.mark.parametrize('to_import', [
    'print_function'
    'custom_value',
])
def test_wrong_future_import(assert_errors, parse_ast_tree, code, to_import):
    """Testing that future imports are restricted."""
    tree = parse_ast_tree(code.format(to_import))

    visiter = WrongImportVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [FutureImportViolation])


def test_wrong_multiple_future_import(assert_errors, parse_ast_tree):
    """Testing that multiple future imports are restricted."""
    tree = parse_ast_tree("""
    from __future__ import print_function, unicode_literals
    """)

    visiter = WrongImportVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [FutureImportViolation, FutureImportViolation])


@pytest.mark.parametrize('code', [
    future_import,
    future_import_alias,
])
@pytest.mark.parametrize('to_import', FUTURE_IMPORTS_WHITELIST)
def test_correct_future_import(assert_errors, parse_ast_tree, code, to_import):
    """Testing that some future imports are not restricted."""
    tree = parse_ast_tree(code.format(to_import))

    visiter = WrongImportVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [])
