# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    ImportCollisionViolation,
)
from wemake_python_styleguide.violations.consistency import (
    DottedRawImportViolation,
)
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor

# correct
single_import = 'import public'
single_import_from = 'from utils import public'
no_colliding_imports = """
    from other import public
    from other.module import something
"""

similar_imports = """
    import ast
    import astor
"""

no_colliding_imports_from = """
    from utils import public
    from other import something
"""

colliding_import_with_alias = """
    import public
    from public import something as sth
"""

colliding_import_from_with_alias = """
    from utils import public
    from utils.public.others import something as sth
"""

# wrong
colliding_import_name_module = """
    import public
    from public import something
"""

colliding_import_name_module_part = """
    import public
    from public.module import something
"""

colliding_multiple_imports = """
    import public, foo, bar as baz
    from public.module import something
"""

colliding_imports_from = """
    from utils import public
    from utils.public.module import something
"""

colliding_multiple_imports_from0 = """
    from utils import public, foo, bar as baz
    from utils.public import something
"""

colliding_multiple_imports_from1 = """
    from utils import public
    from utils.public.module import something as sth, something_else
"""


@pytest.mark.parametrize('code', [
    single_import,
    single_import_from,
    no_colliding_imports,
    similar_imports,
    no_colliding_imports_from,
    colliding_import_with_alias,
    colliding_import_from_with_alias,
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

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    colliding_import_name_module,
    colliding_import_name_module_part,
    colliding_multiple_imports,
    colliding_imports_from,
    colliding_multiple_imports_from0,
    colliding_multiple_imports_from1,
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

    assert_errors(visitor, [ImportCollisionViolation])


def test_collision_in_single_import_statement(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing that colliding imports in one import statement are restricted."""
    tree = parse_ast_tree('import abc, abc.ABC')

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [DottedRawImportViolation, ImportCollisionViolation],
    )
