# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.general.wrong_module import (
    InitModuleHasLogicViolation,
    WrongContentsVisitor,
)

empty_module = ''
module_with_docstring = """
'''Hi, am a docstring inside a module.'''
"""

module_with_comments = """
# Some comment about what is going on.
# Commented code:
# print('hi')
"""

module_with_one_import = 'from some import other'
module_with_imports = """
from one import one_func
from two import two_func
"""

module_with_logic = """
try:
    import some
    has_some = True
except ImportError:
    some = None
    has_some = False
"""


@pytest.mark.parametrize('code', [
    empty_module,
    module_with_docstring,
    module_with_comments,
])
def test_init_without_logic(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that `__init__` without logic is allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongContentsVisitor(
        default_options, tree=tree, filename='__init__.py',
    )
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    module_with_imports,
    module_with_one_import,
    module_with_logic,
])
def test_init_with_logic(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that `__init__` with logic is restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongContentsVisitor(
        default_options, tree=tree, filename='__init__.py',
    )
    visitor.run()

    assert_errors(visitor, [InitModuleHasLogicViolation])
