import ast
from typing import Iterable

from typing_extensions import Final

from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.constants import UNUSED_PLACEHOLDER
from wemake_python_styleguide.logic import nodes
from wemake_python_styleguide.logic.naming import name_nodes
from wemake_python_styleguide.logic.tree import classes
from wemake_python_styleguide.types import AnyFunctionDef

#: Prefixes that usually define getters and setters.
_GetterSetterPrefixes: Final = frozenset(('get_', 'set_'))

#: Fixes length of a getter/setter.
GETTER_LENGTH: Final = 4


def find_paired_getters_and_setters(
    node: ast.ClassDef,
) -> Iterable[AnyFunctionDef]:
    """Returns nodes of paired getter or setter methods."""
    stack = {}
    for method in _find_getters_and_setters(node):
        method_stripped = method.name[GETTER_LENGTH:]
        if method_stripped not in stack:
            stack[method_stripped] = method
        else:
            yield method
            paired_method = stack.pop(method_stripped)
            yield paired_method


def find_attributed_getters_and_setters(
    node: ast.ClassDef,
) -> Iterable[AnyFunctionDef]:
    """Returns nodes of attributed getter or setter methods."""
    class_attributes, instance_attributes = classes.get_attributes(
        node,
        include_annotated=True,
    )
    flat_class_attributes = name_nodes.flat_variable_names(class_attributes)

    attributes_stripped = {
        class_attribute.lstrip(UNUSED_PLACEHOLDER)
        for class_attribute in flat_class_attributes
    }.union({
        instance.attr.lstrip(UNUSED_PLACEHOLDER)
        for instance in instance_attributes
    })

    for method in _find_getters_and_setters(node):
        if method.name[GETTER_LENGTH:] in attributes_stripped:
            yield method


def _find_getters_and_setters(node: ast.ClassDef) -> Iterable[AnyFunctionDef]:
    """Returns nodes of all getter or setter methods."""
    for sub in ast.walk(node):
        is_correct_context = nodes.get_context(sub) is node
        if isinstance(sub, FunctionNodes) and is_correct_context:
            if sub.name[:GETTER_LENGTH] in _GetterSetterPrefixes:
                yield sub
