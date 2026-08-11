import ast

import pytest

from wemake_python_styleguide.compat.constants import PY315
from wemake_python_styleguide.logic.tree.imports import is_lazy_import

if not PY315:  # pragma: >=3.15 no cover
    pytest.skip(  # pragma: no cover
        reason='lazy imports were added in python 3.15+',
        allow_module_level=True,
    )


def test_lazy_import():
    """Check that lazy imports are detected."""
    node = ast.Import(names=[ast.alias(name='a')], is_lazy=1)
    assert is_lazy_import(node)


def test_regular_import():
    """Check that regular imports are not detected."""
    assert not is_lazy_import(ast.Import(names=[ast.alias(name='a')]))
