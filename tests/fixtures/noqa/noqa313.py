"""
This file contains all possible violations for python 3.13+.

It is used for e2e tests.
"""

class NewStyleGenerics[
    TypeVarDefault=int,
    *FollowingTuple=*tuple[int, ...]  # noqa: WPS477
]:
    """TypeVarTuple follows a defaulted TypeVar."""
