import pytest

from wemake_python_styleguide.violations.best_practices import (
    ImportCollisionViolation,
)
from wemake_python_styleguide.violations.consistency import (
    DottedRawImportViolation,
    LocalFolderImportViolation,
)
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor

# Correct:

correct_single_import = 'import public'
correct_single_import_from = 'from utils import public'
correct_no_colliding_imports = """
from other import public
from other.module import something
"""

correct_similar_imports = """
import ast
import astor
"""

correct_no_colliding_imports_from = """
from utils import public
from other import something
"""

correct_import_with_alias = """
import public
from public import something as sth
"""

correct_import_from_with_alias = """
from utils import public
from utils.public.others import something as sth
"""

correct_multiple_imports_from = """
from utils import public
from utils.public.module import something as sth, something_else
"""

correct_imports_from = """
from utils import public
from utils.public.module import something
"""

correct_import_name_module_part = """
import public
from public.module import something
"""

correct_relative_import = """
from . import first as _my
from first import other
"""

# Wrong:

colliding_same_line = 'import abc, abc.ABC'
colliding_import_name_module = """
import public
from public import something
"""

colliding_multiple_imports = """
import public, foo, bar as baz
from public import something
"""

colliding_multiple_imports_from = """
from utils import public, foo, bar as baz
from utils.public import something
"""

colliding_relative_import1 = """
from . import first
from first import other
"""

colliding_relative_import2 = """
from .. import first
from first import other
"""


@pytest.mark.parametrize('code', [
    correct_single_import,
    correct_single_import_from,
    correct_no_colliding_imports,
    correct_similar_imports,
    correct_no_colliding_imports_from,
    correct_import_with_alias,
    correct_import_from_with_alias,
    correct_multiple_imports_from,
    correct_imports_from,
    correct_import_name_module_part,
    correct_relative_import,
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

    assert_errors(visitor, [], ignored_types=LocalFolderImportViolation)


@pytest.mark.parametrize('code', [
    colliding_same_line,
    colliding_import_name_module,
    colliding_multiple_imports,
    colliding_multiple_imports_from,
    colliding_relative_import1,
    colliding_relative_import2,
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
        [ImportCollisionViolation],
        ignored_types=(DottedRawImportViolation, LocalFolderImportViolation),
    )
