import ast
from typing import Union

from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.constants import SPECIAL_ARGUMENT_NAMES_WHITELIST
from wemake_python_styleguide.logic import nodes, walk
from wemake_python_styleguide.logic.arguments import call_args

#: Nodes that can be annotated.
_AnnNodes = (ast.AnnAssign, ast.arg)


def is_class_context(node: ast.AST) -> bool:
    """
    Detects if a node is inside a class context.

    We use this predicate because classes have quite complex
    DSL to be created: like django-orm, attrs, and dataclasses.
    And these DSLs are built using attributes and calls.
    """
    return isinstance(nodes.get_context(node), ast.ClassDef)


def is_super_call(node: ast.AST) -> bool:
    """
    Detects if super is called.

    We use this predicate because we can call ``super()`` a lot in our code.
    And it is fine.
    """
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        return node.func.id == 'super'
    return False


def is_decorator(node: ast.AST) -> bool:
    """
    Detects if node is used as a decorator.

    We use this predicates because decorators can be used miltiple times.
    Like ``@auth_required(login_url=LOGIN_URL)`` and similar.
    """
    parent = walk.get_closest_parent(node, FunctionNodes)
    if isinstance(parent, FunctionNodes) and parent.decorator_list:
        return any(
            node == decorator or walk.is_contained_by(node, decorator)
            for decorator in parent.decorator_list
        )
    return False


def is_self(node: ast.AST) -> bool:
    """
    Detects if node is ``self``, ``cls``, or ``mcs`` call.

    We use this predicate because we allow a lot of ``self.method()`` or
    ``self[start:end]`` calls. This is fine.

    We do not check for attribute access, because ``ast.Attribute`` nodes
    are globally ignored.
    """
    self_node: Union[ast.Attribute, ast.Subscript, None] = None
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
        self_node = node.func
    elif isinstance(node, ast.Subscript):
        self_node = node

    return bool(
        self_node and
        isinstance(self_node.value, ast.Name) and
        self_node.value.id in SPECIAL_ARGUMENT_NAMES_WHITELIST,
    )


def is_annotation(node: ast.AST) -> bool:
    """
    Detects if node is an annotation. Or a part of it.

    We use this predicate to allow all types of repetetive
    function and instance annotations.
    """
    if not isinstance(node, (ast.Str, ast.List, ast.Tuple, ast.Subscript)):
        return False

    annotated = walk.get_closest_parent(node, (*_AnnNodes, *FunctionNodes))
    if isinstance(annotated, FunctionNodes):
        contains_node = bool(
            annotated.returns and
            walk.is_contained_by(node, annotated.returns),
        )
        return node == annotated.returns or contains_node
    elif isinstance(annotated, _AnnNodes):
        contains_node = bool(
            annotated.annotation and
            walk.is_contained_by(node, annotated.annotation),
        )
        return node == annotated.annotation or contains_node
    return False


def is_primitive(node: ast.AST) -> bool:
    """
    Detects if node is a form of a primitive value.

    We use this predicate to allow values
    like ``[]`` or ``call()`` to be overused.
    Because you cannot simply them.

    We do not check for strings, numbers, etc
    because they are globally ignored.
    """
    if isinstance(node, (ast.Tuple, ast.List)):
        return not node.elts  # we do allow `[]` and `()`
    elif isinstance(node, ast.Set):
        return (  # we do allow `{*set_items}`
            len(node.elts) == 1 and
            isinstance(node.elts[0], ast.Starred)
        )
    elif isinstance(node, ast.Dict):  # we do allow `{}` and `{**values}`
        return not list(filter(None, node.keys))
    elif isinstance(node, ast.Call):
        return not call_args.get_all_args(node)  # we do allow `call()`
    return False
