# -*- coding: utf-8 -*-

"""
Here we store useful aliases to make sure code works between versions.

Please, document everything you do.
Add links to the changes in the changelog if possible.
And provide links to the python source code.
"""

import ast

from typing_extensions import Final

#: We need this tuple to easily check that this is a real assign node.
AssignNodes: Final = (ast.Assign, ast.AnnAssign)
