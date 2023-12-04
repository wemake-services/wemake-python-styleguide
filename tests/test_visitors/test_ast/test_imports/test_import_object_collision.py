import pytest

from wemake_python_styleguide.violations.best_practices import (
    ImportObjectCollisionViolation,
)
from wemake_python_styleguide.violations.consistency import (
    LocalFolderImportViolation,
)
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor

# Correct:

correct_single_import_from = 'from utils import public'
correct_no_colliding_imports = """
from other import public
from other import correct
from third import name1, name2
"""

correct_aliases = """
from other import public as alias1
from my import public as alias2
from third import public
from four.alias1 import public as alias3, other as alias4
"""

correct_same_module_imports = """
from my import name1 as alias1
from my import name2 as alias2
"""

correct_dot_imports = """
from . import sub
from .. import sub as alias1
from ... import sub as alias2
"""

correct_relative_imports = """
from .sub import name
from ..sub import name as alias1
from ...sub import name as alias2
"""

# Wrong:

colliding_object_import1 = """
from module import name, name as alias
"""

colliding_object_import2 = """
from module import name
from module import name as alias
"""

colliding_nested_object_import = """
from module.name import sub
from module.name import sub as alias
"""

colliding_dot_import1 = """
from . import sub
from . import sub as alias
"""

colliding_dot_import2 = """
from ...package import sub
from ...package import sub as alias
"""


@pytest.mark.parametrize('code', [
    correct_single_import_from,
    correct_no_colliding_imports,
    correct_aliases,
    correct_same_module_imports,
    correct_dot_imports,
    correct_relative_imports,
])
def test_correct_imports(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that no colliding imports are allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [], ignored_types=(LocalFolderImportViolation,))


@pytest.mark.parametrize('code', [
    colliding_object_import1,
    colliding_object_import2,
    colliding_nested_object_import,
])
def test_imports_collision(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that colliding imports are restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [ImportObjectCollisionViolation],
        ignored_types=(LocalFolderImportViolation,),
    )
