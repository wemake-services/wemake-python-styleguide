import ast
from typing import Dict, Optional


def is_ordinary_super_call(node: ast.AST, class_name: str) -> bool:
    """
    Tells whether super ``call`` is ordinary.

    By ordinary we mean:

    - either call without arguments::

        super().function()

    - or call with our class and self arguments::

        super(Class, self).function()

    Any other combination of arguments is considered as expected by
    this function.
    """
    call = _get_super_call(node)
    if call is None:
        return False
    args_number = len(call.args) + len(call.keywords)
    if args_number == 0:
        return True
    return args_number == 2 and _is_super_called_with(
        call,
        type_=class_name,
        object_='self',
    )


def _get_keyword_args_by_names(
    call: ast.Call,
    *names: str,
) -> Dict[str, ast.expr]:
    """Returns keywords of ``call`` by specified ``names``."""
    keyword_args = {}
    for keyword in call.keywords:
        if keyword.arg in names:
            keyword_args[keyword.arg] = keyword.value
    return keyword_args


def _is_super_called_with(call: ast.Call, type_: str, object_: str) -> bool:
    """Tells whether super ``call`` was done with ``type_`` and ``object_``."""
    if len(call.args) == 2:  # branch for super(Test, self)
        arg1: Optional[ast.expr] = call.args[0]
        arg2: Optional[ast.expr] = call.args[1]
    elif len(call.keywords) == 2:  # branch for super(t=Test, obj=self)
        keyword_args = _get_keyword_args_by_names(call, 't', 'obj')
        arg1 = keyword_args.get('t')
        arg2 = keyword_args.get('obj')
    else:  # branch for super(Test, obj=self)
        arg1 = call.args[0]
        arg2 = call.keywords[0].value
    is_expected_type = isinstance(arg1, ast.Name) and arg1.id == type_
    is_expected_object = isinstance(arg2, ast.Name) and arg2.id == object_
    return is_expected_type and is_expected_object


def _get_super_call(node: ast.AST) -> Optional[ast.Call]:
    """Returns given ``node`` if it represents ``super`` ``ast.Call``."""
    if not isinstance(node, ast.Call):
        return None
    if not isinstance(node.func, ast.Name) or node.func.id != 'super':
        return None
    return node
