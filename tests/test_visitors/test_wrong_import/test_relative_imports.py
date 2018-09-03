# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.wrong_import import (
    LocalFolderImportViolation,
    WrongImportVisitor,
)

same_level_relative_import = """
from . import some
"""

same_level_relative_import_sibling = """
from .some import MyClass
"""

parent_level_relative_import = """
from .. import some
"""

parent_level_relative_import_sibling = """
from ..some import MyClass
"""


@pytest.mark.parametrize('code', [
    same_level_relative_import,
    same_level_relative_import_sibling,
    parent_level_relative_import,
    parent_level_relative_import_sibling,
])
def test_local_folder_import(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that relative to local folder imports are restricted."""
    tree = parse_ast_tree(code)

    visiter = WrongImportVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [LocalFolderImportViolation])


def test_regular_import(assert_errors, parse_ast_tree, default_options):
    """Testing that regular imports are allowed."""
    tree = parse_ast_tree('import os')

    visiter = WrongImportVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [])


def test_regular_from_import(assert_errors, parse_ast_tree, default_options):
    """Testing that regular from imports are allowed."""
    tree = parse_ast_tree('from os import path')

    visiter = WrongImportVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [])
