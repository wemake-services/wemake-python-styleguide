import pytest

from wemake_python_styleguide.visitors.decorators import alias


class _HasAliasedProp(object):
    def existing(self):
        """Existing."""

    def first(self):
        """First."""


def test_raises_for_duplicates():
    """Ensures that decorator raises an exception for duplicates."""
    with pytest.raises(ValueError, match='duplicate'):
        alias('name', ('duplicate', 'duplicate'))


def test_useless_alias():
    """Ensures that decorator raises an exception for duplicates."""
    with pytest.raises(ValueError, match='duplicate'):
        alias('name', ('name',))


def test_raises_for_missing_alias():
    """Ensures that decorator raises an exception for missing alias."""
    with pytest.raises(AttributeError):
        alias('new_alias', ('first', 'second'))(_HasAliasedProp)


def test_raises_for_existing_alias():
    """Ensures that decorator raises an exception for existing alias."""
    with pytest.raises(AttributeError):
        alias('existing', ('first', 'second'))(_HasAliasedProp)
