from collections.abc import Callable
from typing import TypeVar

_DefinedType = TypeVar('_DefinedType')


def _modify_class(
    cls: type[_DefinedType],
    original: str,
    aliases: tuple[str, ...],
) -> type[_DefinedType]:
    original_handler = getattr(cls, original, None)
    if original_handler is None:
        raise AttributeError(
            f'Aliased attribute {original} does not exist',
        )

    for method_alias in aliases:
        if getattr(cls, method_alias, None):
            raise AttributeError(
                f'Alias {method_alias} already exists',
            )
        setattr(cls, method_alias, original_handler)
    return cls


def alias(
    original: str,
    aliases: tuple[str, ...],
) -> Callable[[type[_DefinedType]], type[_DefinedType]]:
    """
    Decorator to alias handlers.

    Why do we need it?
    Because there are cases when we need to use the same method to
    handle different nodes types.

    We can just create aliases like ``visit_Import = visit_ImportFrom``,
    but it looks verbose and ugly.
    """
    all_names = (*aliases, original)
    if len(all_names) != len(set(all_names)):
        raise ValueError('Found duplicate aliases')

    def decorator(cls: type[_DefinedType]) -> type[_DefinedType]:
        return _modify_class(cls, original, aliases)

    return decorator
