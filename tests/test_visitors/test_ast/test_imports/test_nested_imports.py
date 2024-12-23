import pytest

from wemake_python_styleguide.compat.constants import PY311
from wemake_python_styleguide.violations.best_practices import (
    NestedImportViolation,
)
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor

# Wrong imports:

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

nested_try_star_import = """
try:
    from missing import some_thing
except* ImportError:
    some_thing = None
"""

nested_import_in_for_loop = """
for _ in range():
    from missing import some_thing
"""

nested_try_import_in_function = """
def function():
    try:
        from missing import some_thing
    except ImportError:
        some_thing = None
"""

nested_try_star_import_in_function = """
def function():
    try:
        from missing import some_thing
    except* ImportError:
        some_thing = None
"""

# Correct imports:

regular_import = 'import os'
regular_from_import = 'from os import path'
regular_nested_import = 'from core.violations import Error'

type_checking_import = """
if TYPE_CHECKING:
    from core.violations import Error
"""

typing_type_checking_import = """
if typing.TYPE_CHECKING:
    from core.violations import Error
"""

nested_try_import = """
try:
    from missing import some_thing
except ImportError:
    some_thing = None
"""


@pytest.mark.parametrize(
    'code',
    [
        nested_function_import,
        nested_function_from_import,
        nested_method_import,
        nested_method_from_import,
        nested_conditional_import,
        nested_import_in_for_loop,
        pytest.param(
            nested_try_star_import,
            marks=[
                pytest.mark.skipif(
                    not PY311, reason='ExceptionGroups were added in 3.11'
                )
            ],
        ),
        nested_try_import_in_function,
        pytest.param(
            nested_try_star_import_in_function,
            marks=[
                pytest.mark.skipif(
                    not PY311, reason='ExceptionGroups were added in 3.11'
                )
            ],
        ),
    ],
)
def test_nested_import(assert_errors, parse_ast_tree, code, default_options):
    """Testing that nested imports are restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NestedImportViolation])


@pytest.mark.parametrize(
    'code',
    [
        regular_import,
        regular_from_import,
        regular_nested_import,
        type_checking_import,
        typing_type_checking_import,
        nested_try_import,
    ],
)
def test_regular_imports(assert_errors, parse_ast_tree, code, default_options):
    """
    Testing imports that are allowed.

    Regular imports are allowed.
    Imports nested inside the TYPE_CHECKING check are allowed.
    """
    tree = parse_ast_tree(code)

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
