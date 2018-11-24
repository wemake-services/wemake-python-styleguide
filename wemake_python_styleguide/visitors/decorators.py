# -*- coding: utf-8 -*-

from typing import Callable, Tuple


def alias(
    original: str,
    aliases: Tuple[str, ...],
) -> Callable[[type], type]:
    """
    Decorator to alias handlers.

    Why do we need it?
    Because there are cases when we need to use the same method to
    handle different nodes types.

    We can just create aliases like ``visit_Import = visit_ImportFrom``,
    but it looks verbose and ugly.
    """
    if len(aliases) != len(set(aliases)):
        raise ValueError('Found duplicate aliases')

    def decorator(cls: type) -> type:
        original_handler = getattr(cls, original)
        for alias in aliases:
            setattr(cls, alias, original_handler)
        return cls
    return decorator
