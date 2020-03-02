from typing import Callable, Tuple, Type, TypeVar

_DefinedType = TypeVar('_DefinedType')


def _modify_class(
    cls: Type[_DefinedType],
    original: str,
    aliases: Tuple[str, ...],
) -> Type[_DefinedType]:
    original_handler = getattr(cls, original, None)
    if original_handler is None:
        raise AttributeError(
            'Aliased attribute {0} does not exist'.format(original),
        )

    for method_alias in aliases:
        if getattr(cls, method_alias, None):
            raise AttributeError(
                'Alias {0} already exists'.format(method_alias),
            )
        setattr(cls, method_alias, original_handler)
    return cls


def alias(
    original: str,
    aliases: Tuple[str, ...],
) -> Callable[[Type[_DefinedType]], Type[_DefinedType]]:
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

    def decorator(cls: Type[_DefinedType]) -> Type[_DefinedType]:
        return _modify_class(cls, original, aliases)
    return decorator
