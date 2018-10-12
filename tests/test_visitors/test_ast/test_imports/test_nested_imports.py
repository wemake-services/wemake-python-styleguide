# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    NestedImportViolation,
)
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor

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
    from missing import some_thing
except ImportError:
    some_thing = None
"""

# Correct imports:

regular_import = 'import os'
regular_from_import = 'from os import path'
regular_nested_import = 'from core.violations import Error'


@pytest.mark.parametrize('code', [
    nested_function_import,
    nested_function_from_import,
    nested_method_import,
    nested_method_from_import,
    nested_conditional_import,
    nested_try_import,
])
def test_nested_import(assert_errors, parse_ast_tree, code, default_options):
    """Testing that nested imports are restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NestedImportViolation])


@pytest.mark.parametrize('code', [
    regular_import,
    regular_from_import,
    regular_nested_import,
])
def test_regular_imports(assert_errors, parse_ast_tree, code, default_options):
    """Testing that regular imports are allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
