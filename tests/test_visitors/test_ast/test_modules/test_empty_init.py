import pytest

from wemake_python_styleguide.violations.best_practices import (
    InitModuleHasLogicViolation,
)
from wemake_python_styleguide.visitors.ast.modules import (
    EmptyModuleContentsVisitor,
)

empty_module = ''
module_with_docstring = """
'''Hi, am a docstring inside a module.'''
"""

module_with_comments = """
# Some comment about what is going on.
# Commented code:
# print('hi')  # noqa: E800
"""

module_with_one_import = 'from some_module import other'
module_with_imports = """
from one import one_func
from two import two_func
"""

module_with_docstring_and_import = """
'''Hi, am a docstring inside a module.'''

from some_module import other
import some_module
"""

module_with_multiple_statements = 'x = 1\ny = 2'
module_with_logic = """
try:
    import some_module
    has_some = True
except ImportError:
    some_module = None
    has_some = False
"""


@pytest.mark.parametrize(
    'code',
    [
        empty_module,
        module_with_docstring,
        module_with_comments,
        module_with_imports,
        module_with_one_import,
        module_with_docstring_and_import,
    ],
)
def test_init_without_logic(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that `__init__` without logic is allowed."""
    tree = parse_ast_tree(code)

    visitor = EmptyModuleContentsVisitor(
        default_options,
        tree=tree,
        filename='__init__.py',
    )
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        module_with_logic,
        module_with_multiple_statements,
    ],
)
def test_init_with_logic(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that `__init__` with logic is restricted."""
    tree = parse_ast_tree(code)

    visitor = EmptyModuleContentsVisitor(
        default_options,
        tree=tree,
        filename='__init__.py',
    )
    visitor.run()

    assert_errors(visitor, [InitModuleHasLogicViolation])
