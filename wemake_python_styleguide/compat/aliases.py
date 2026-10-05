"""
Here we store useful aliases to make sure code works between versions.

Please, document everything you do.
Add links to the changes in the changelog if possible.
And provide links to the python source code.
"""

import ast
from typing import Final, final


@final
class _TextNodesMeta(type):
    def __instancecheck__(cls, instance):
        return isinstance(instance, ast.Constant) and isinstance(
            instance.value,
            str | bytes,
        )


@final
class TextNodes(ast.AST, metaclass=_TextNodesMeta):
    """Check if node has type of `ast.Constant` with `str` or `bytes`."""

    value: str | bytes  # noqa: WPS110


AssignNodes: Final = (ast.Assign, ast.AnnAssign)
"""We need this tuple to easily check that this is a real assign node."""

AssignNodesWithWalrus: Final = (*AssignNodes, ast.NamedExpr)
"""We need this tuple for cases where we use full assign power."""

FunctionNodes: Final = (ast.FunctionDef, ast.AsyncFunctionDef)
"""We need this tuple since ``async def`` now has its own ast class."""

ForNodes: Final = (ast.For, ast.AsyncFor)
"""We need this tuple since ``ast.AsyncFor``` was introduced."""

WithNodes: Final = (ast.With, ast.AsyncWith)
"""We need this tuple since ``ast.AsyncWith`` was introduced."""
