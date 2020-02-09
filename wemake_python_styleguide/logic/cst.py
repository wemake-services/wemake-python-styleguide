from libcst import BaseParenthesizableWhitespace, SimpleWhitespace


def not_empty_whitespace(node: BaseParenthesizableWhitespace) -> bool:
    """
    ...
    """

    return isinstance(node, SimpleWhitespace) and node.value
