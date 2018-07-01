# -*- coding: utf-8 -*-

from wemake_python_styleguide.visitors.wrong_import import (
    DynamicImportViolation,
    WrongImportVisitor,
)


def test_dynamic_import(assert_errors, parse_ast_tree):
    """Testing that relative to local folder imports are restricted."""
    tree = parse_ast_tree("module = __import__('os')")

    visiter = WrongImportVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [DynamicImportViolation])


def test_importlib_import(assert_errors, parse_ast_tree):
    """Testing that importlib imports are allowed."""
    tree = parse_ast_tree("""
    import importlib
    importlib.import_module('os')
    """)

    visiter = WrongImportVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [])
