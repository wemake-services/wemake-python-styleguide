from ast import Call, Return, Yield, YieldFrom, arg, walk
from typing import Container, Iterable, List, Tuple, Type, Union

from typing_extensions import Final

from wemake_python_styleguide.compat.functions import get_posonlyargs
from wemake_python_styleguide.logic import source
from wemake_python_styleguide.logic.walk import is_contained
from wemake_python_styleguide.types import (
    AnyFunctionDef,
    AnyFunctionDefAndLambda,
)

#: Expressions that causes control transfer from a routine
_AnyControlTransfers = Union[
    Return,
    Yield,
    YieldFrom,
]

#: Type annotation for an iterable of control transfer nodes
_ControlTransferIterable = Iterable[_AnyControlTransfers]

#: Type annotation for a tuple of control transfer nodes
_ControlTransferTuple = Tuple[
    Type[Return],
    Type[Yield],
    Type[YieldFrom],
]

#: Method types
_METHOD_TYPES: Final = frozenset((
    'method',
    'classmethod',
    'staticmethod',
))


def given_function_called(
    node: Call,
    to_check: Container[str],
    *,
    split_modules: bool = False,
) -> str:
    """
    Returns function name if it is called and contained in the container.

    If `split_modules`, takes the modules or objects into account. Otherwise,
    it only cares about the function's name.
    """
    function_name = source.node_to_string(node.func)
    if split_modules:
        function_name = function_name.split('.')[-1]
    if function_name in to_check:
        return function_name
    return ''


def is_method(function_type: str) -> bool:
    """
    Returns whether a given function type belongs to a class.

    >>> is_method('function')
    False

    >>> is_method(None)
    False

    >>> is_method('method')
    True

    >>> is_method('classmethod')
    True

    >>> is_method('staticmethod')
    True

    >>> is_method('')
    False

    """
    return function_type in _METHOD_TYPES


def get_all_arguments(node: AnyFunctionDefAndLambda) -> List[arg]:
    """
    Returns list of all arguments that exist in a function.

    Respects the correct parameters order.
    Positional only args, regular argument,
    ``*args``, keyword-only, ``**kwargs``.

    Positional only args are only added for ``python3.8+``
    other versions are ignoring this type of arguments.
    """
    names = [
        *get_posonlyargs(node),
        *node.args.args,
    ]

    if node.args.vararg:
        names.append(node.args.vararg)

    names.extend(node.args.kwonlyargs)

    if node.args.kwarg:
        names.append(node.args.kwarg)

    return names


def is_first_argument(node: AnyFunctionDefAndLambda, name: str) -> bool:
    """Tells whether an argument name is the logically first in function."""
    positional_args = [
        *get_posonlyargs(node),
        *node.args.args,
    ]

    if not positional_args:
        return False

    return name == positional_args[0].arg


def is_generator(node: AnyFunctionDef) -> bool:
    """Tells whether a given function is a generator."""
    for body_item in node.body:
        if is_contained(node=body_item, to_check=(Yield, YieldFrom)):
            return True
    return False


def get_function_exit_nodes(node: AnyFunctionDef) -> _ControlTransferIterable:
    """Yields nodes that cause a control transfer from a function."""
    control_transfer_nodes = (Return, Yield, YieldFrom)
    for body_item in node.body:
        for sub_node in walk(body_item):
            if isinstance(sub_node, control_transfer_nodes):
                yield sub_node
