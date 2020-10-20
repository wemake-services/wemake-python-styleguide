"""
Here we store useful aliases to make sure code works between versions.

Please, document everything you do.
Add links to the changes in the changelog if possible.
And provide links to the python source code.
"""

import ast

from typing_extensions import Final

from wemake_python_styleguide.compat.nodes import NamedExpr

#: We need this tuple to easily work with both types of text nodes:
TextNodes: Final = (ast.Str, ast.Bytes)

#: We need this tuple to easily check that this is a real assign node.
AssignNodes: Final = (ast.Assign, ast.AnnAssign)

#: We need this tuple for cases where we use full assign power.
AssignNodesWithWalrus: Final = (*AssignNodes, NamedExpr)

#: We need this tuple since ``async def`` now has its own ast class.
FunctionNodes: Final = (ast.FunctionDef, ast.AsyncFunctionDef)

#: We need this tuple since ``ast.AsyncFor``` was introduced.
ForNodes: Final = (ast.For, ast.AsyncFor)

#: We need this tuple since ``ast.AsyncWith`` was introduced.
WithNodes: Final = (ast.With, ast.AsyncWith)
