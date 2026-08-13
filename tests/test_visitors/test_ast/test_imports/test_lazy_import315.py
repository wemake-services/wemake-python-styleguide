import pytest

from wemake_python_styleguide.compat.constants import PY315
from wemake_python_styleguide.violations.best_practices import (
    ForbidLazyImportViolation,
)
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor

if not PY315:  # pragma: >=3.15 no cover
    pytest.skip(  # pragma: no cover
        reason='lazy imports were added in python 3.15+',
        allow_module_level=True,
    )


@pytest.mark.parametrize(
    'code',
    [
        'lazy from json import dumps',
        'lazy import json',
    ],
)
def test_imports_collision(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that lazy imports are restricted."""
    tree = parse_ast_tree(code)

    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [ForbidLazyImportViolation],
    )
