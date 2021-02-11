import tokenize
from typing import Container, Iterable


def only_contains(
    tokens: Iterable[tokenize.TokenInfo],
    container: Container[int],
) -> bool:
    """Determines that only tokens from the given list are contained."""
    return all(
        token.exact_type in container
        for token in tokens
    )
