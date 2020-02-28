from wemake_python_styleguide.logic.naming.access import is_unused


def is_constant(name: str) -> bool:
    """
    Checks whether the given ``name`` is a constant.

    >>> is_constant('CONST')
    True

    >>> is_constant('ALLOWED_EMPTY_LINE_TOKEN')
    True

    >>> is_constant('Some')
    False

    >>> is_constant('_')
    False

    >>> is_constant('lower_case')
    False

    """
    if is_unused(name):
        return False

    return all(
        # We check that constant names consist of:
        # UPPERCASE LETTERS and `_` char
        character.isupper() or character == '_'
        for character in name
    )
