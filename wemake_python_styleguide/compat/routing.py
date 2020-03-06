import ast
import types

from typing_extensions import Final

from wemake_python_styleguide.compat.constants import PY38
from wemake_python_styleguide.compat.nodes import Constant

#: That's how python types and ast types map to each other, copyied from ast.
_CONST_NODE_TYPE_NAMES: Final = types.MappingProxyType({
    bool: 'NameConstant',  # should be before int
    type(None): 'NameConstant',
    int: 'Num',
    float: 'Num',
    complex: 'Num',
    str: 'Str',
    bytes: 'Bytes',
    type(...): 'Ellipsis',
})


if PY38:  # pragma: py-lt-38
    def route_visit(self: ast.NodeVisitor, node: ast.AST):
        """
        Custom router for python3.8+ release.

        Hacked to make sure that everything we had defined before is working.
        """
        if isinstance(node, Constant):
            # That's the hack itself, we don't get the name of the node.
            # We get the name of wrapped type from it.
            type_name = _CONST_NODE_TYPE_NAMES.get(type(node.value))
        else:
            type_name = node.__class__.__name__

        return getattr(
            self,
            'visit_{0}'.format(type_name),
            self.generic_visit,
        )(node)

else:  # pragma: py-gte-38
    route_visit = ast.NodeVisitor.visit  # noqa: WPS440
