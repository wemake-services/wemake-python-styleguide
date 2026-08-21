import pytest

from wemake_python_styleguide.compat.constants import PY315
from wemake_python_styleguide.violations.best_practices import (
    ForbidMappingProxyTypeViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    WrongFunctionCallVisitor,
)

pytestmark = pytest.mark.skipif(
    not PY315,
    reason='frozendict were added in python 3.15+',
)


@pytestmark
@pytest.mark.parametrize(
    'code',
    [
        'MappingProxyType({"a": 1})',
        'MappingProxyType({"a": 1, "b": 2})',
        'import types\ntypes.MappingProxyType({"a": 1})',
        'types.MappingProxyType({"a": 1})',
    ],
)
def test_mapping_proxy_type(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that ``MappingProxyType`` is forbidden."""
    tree = parse_ast_tree(code)
    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [ForbidMappingProxyTypeViolation],
    )
