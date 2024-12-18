import ast
from typing import Final

_ENUM_NAMES: Final = (
    'enum.Enum',
    'enum.EnumType',
    'enum.EnumMeta',
    'Enum',
    'EnumType',
    'EnumMeta',
)


def has_enum_base(defn: ast.ClassDef) -> bool:
    """Tells whether some class has `Enum` or similar class as its base."""
    string_bases = {ast.unparse(base) for base in defn.bases}
    return any(enum_base in string_bases for enum_base in _ENUM_NAMES)
