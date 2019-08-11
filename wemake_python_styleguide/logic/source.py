# -*- coding: utf-8 -*-

import ast

import astor


def node_to_string(node: ast.AST) -> str:
    """Returns the source code by doing ``ast`` to string convert."""
    return astor.to_source(node).strip()
