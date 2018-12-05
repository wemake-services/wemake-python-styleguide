# -*- coding: utf-8 -*-

import tokenize
from typing import Container, Iterable


def only_contains(
    tokens: Iterable[tokenize.TokenInfo],
    container: Container[int],
) -> bool:
    """Determins that only tokens from the given list are contained."""
    for token in tokens:
        if token.exact_type not in container:
            return False
    return True
