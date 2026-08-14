import sys
import types
from collections.abc import Mapping
from typing import Final, TypeVar

_KT = TypeVar('_KT')
_VT = TypeVar('_VT')

#: This indicates that we are running on python3.11+
PY311: Final = sys.version_info >= (3, 11)

# This indicates that we are running on python3.12+
PY312: Final = sys.version_info >= (3, 12)

# This indicates that we are running on python3.13+
PY313: Final = sys.version_info >= (3, 13)

# This indicates that we are running on python3.15+
PY315: Final = sys.version_info >= (3, 15)


def make_immutable(
    mutable_dict: Mapping[_KT, _VT],
) -> Mapping[_KT, _VT]:
    """Make a dictionary immutable."""
    if PY315:  # pragma: >=3.15 cover
        return frozendict(mutable_dict)  # noqa: F821
    return types.MappingProxyType(mutable_dict)  # noqa: WPS483 # pragma: <3.15 cover
