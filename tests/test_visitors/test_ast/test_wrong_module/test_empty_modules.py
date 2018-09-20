# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.wrong_module import (
    EmptyModuleViolation,
    WrongContentsVisitor,
)


@pytest.mark.parametrize('filename', [
    'empty.py',
    '/home/user/logics.py',
    'partial/views.py',
    'C:/path/package/module.py',
])
def test_simple_filename(
    assert_errors, parse_ast_tree, filename, default_options,
):
    """Testing that simple file names should not be empty."""
    tree = parse_ast_tree('')

    visitor = WrongContentsVisitor(
        default_options, tree=tree, filename=filename,
    )
    visitor.run()

    assert_errors(visitor, [EmptyModuleViolation])
