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
    all_names = aliases + (original, )
    if len(all_names) != len(set(all_names)):
        raise ValueError('Found duplicate aliases')

    def decorator(cls: type) -> type:
        original_handler = getattr(cls, original, None)
        if original_handler is None:
            raise AttributeError('Aliased attribute {0} does not exist'.format(
                original,
            ))

        for method_alias in aliases:
            if getattr(cls, method_alias, None):
                raise AttributeError(
                    'Alias {0} already exists'.format(method_alias),
                )
            setattr(cls, method_alias, original_handler)

        return cls
    return decorator
