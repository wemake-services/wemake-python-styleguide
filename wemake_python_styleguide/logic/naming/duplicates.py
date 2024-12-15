from functools import reduce


def get_duplicate_names(variables: list[set[str]]) -> set[str]:
    """
    Find duplicate names in different nodes.

    >>> get_duplicate_names([{'a', 'b'}, {'b', 'c'}])
    {'b'}
    """
    return reduce(
        lambda acc, element: acc.intersection(element),
        variables,
    )
