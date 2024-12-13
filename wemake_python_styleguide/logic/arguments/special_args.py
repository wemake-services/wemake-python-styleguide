import ast

from wemake_python_styleguide import constants, types


def clean_special_argument(
    node: types.AnyFunctionDefAndLambda,
    node_args: list[ast.arg],
) -> list[ast.arg]:
    """Removes ``self``, ``cls``, ``mcs`` from argument lists."""
    if not node_args or isinstance(node, ast.Lambda):
        return node_args
    if node_args[0].arg not in constants.SPECIAL_ARGUMENT_NAMES_WHITELIST:
        return node_args
    return node_args[1:]
