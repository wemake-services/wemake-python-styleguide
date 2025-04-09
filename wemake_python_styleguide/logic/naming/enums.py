import ast
from collections.abc import Collection
from typing import Final

from wemake_python_styleguide.logic.source import node_to_string

_CONCRETE_ENUM_NAMES: Final = (
    'enum.StrEnum',
    'StrEnum',
    'enum.IntEnum',
    'IntEnum',
    'enum.IntFlag',
    'IntFlag',
)

_REGULAR_ENUM_NAMES: Final = (
    'enum.Enum',
    'enum.EnumType',
    'enum.EnumMeta',
    'Enum',
    'EnumType',
    'EnumMeta',
    'enum.Flag',
    'Flag',
    'enum.ReprEnum',
    'ReprEnum',
)

_ENUM_NAMES: Final = (
    *_CONCRETE_ENUM_NAMES,
    *_REGULAR_ENUM_NAMES,
)

_ENUM_LIKE_NAMES: Final = (
    *_ENUM_NAMES,
    'Choices',
    'models.Choices',
    'IntegerChoices',
    'models.IntegerChoices',
    'TextChoices',
    'models.TextChoices',
)


def _has_one_of_base_classes(
    defn: ast.ClassDef, base_names: Collection[str]
) -> bool:
    """Tells whether some class has one of provided names as its base."""
    string_bases = {node_to_string(base) for base in defn.bases}
    return any(enum_base in string_bases for enum_base in base_names)


def has_regular_enum_base(defn: ast.ClassDef) -> bool:
    """Tells whether some class has `Enum` or similar class as its base.

    Excluded `IntEnum`, `StrEnum`, `IntFlag` concrete `Enum` subclasses.
    Because those classes have already been subclassed using primitives.
    """
    return _has_one_of_base_classes(defn, _REGULAR_ENUM_NAMES)


def has_enum_like_base(defn: ast.ClassDef) -> bool:
    """
    Tells if some class has `Enum` or semantically similar class as its base.

    Unlike ``has_enum_base`` it also includes support for Django Choices.
    https://docs.djangoproject.com/en/5.1/ref/models/fields/#choices
    """
    return _has_one_of_base_classes(defn, _ENUM_LIKE_NAMES)
