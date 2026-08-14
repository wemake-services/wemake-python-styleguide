import pytest

from wemake_python_styleguide.compat.constants import PY315
from wemake_python_styleguide.violations.best_practices import (
    ForbidLazyImportViolation,
)
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor

pytestmark = pytest.mark.skipif(
    not PY315,
    reason='lazy imports were added in python 3.15+',
)


@pytestmark
@pytest.mark.parametrize(
    'code',
    [
        'lazy from json import dumps as json_dumps',
        'lazy import json',
    ],
)
def test_lazy_import(
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
