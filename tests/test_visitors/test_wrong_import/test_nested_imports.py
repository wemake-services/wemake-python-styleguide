# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.wrong_import import (
    NestedImportViolation,
    WrongImportVisitor,
)

# Incorrect imports:

nested_function_import = """
def function():
    import os
"""

nested_function_from_import = """
def function():
    from os import path
"""

nested_conditional_import = """
if True:
    import os
"""

nested_method_import = """
class Test:
    def with_import(self):
        import os
"""

nested_method_from_import = """
class Test:
    def with_import(self):
        from os import path
"""

nested_try_import = """
try:
    from missing import some
except ImportError:
    some = None
"""

# Correct imports:

regular_import = """
import os
"""

regular_from_import = """
from os import path
"""


@pytest.mark.parametrize('code', [
    nested_function_import,
    nested_function_from_import,
    nested_method_import,
    nested_method_from_import,
    nested_conditional_import,
    nested_try_import,
])
def test_nested_import(assert_errors, parse_ast_tree, code):
    """Testing that nested imports are restricted."""
    tree = parse_ast_tree(code)

    visiter = WrongImportVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [NestedImportViolation])


@pytest.mark.parametrize('code', [
    regular_import,
    regular_from_import,
])
def test_regular_imports(assert_errors, parse_ast_tree, code):
    """Testing that regular imports are allowed."""
    tree = parse_ast_tree(code)

    visiter = WrongImportVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [])
