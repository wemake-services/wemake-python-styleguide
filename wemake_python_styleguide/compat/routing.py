# -*- coding: utf-8 -*-

import ast
import types

from typing_extensions import Final

from wemake_python_styleguide.compat.constants import PY38

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
        if isinstance(node, ast.Constant):
            type_name = _CONST_NODE_TYPE_NAMES.get(type(node.value), None)
            if type_name is not None:
                return getattr(
                    self,
                    'visit_{0}'.format(type_name),
                    self.generic_visit,
                )(node)
        return self.generic_visit(node)
else:  # pragma: py-gte-38
    route_visit = ast.NodeVisitor.visit  # noqa: WPS440
