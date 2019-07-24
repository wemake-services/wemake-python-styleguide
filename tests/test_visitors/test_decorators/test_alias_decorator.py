# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.decorators import alias


def test_raises_for_duplicates():
    """Ensures that decorator raises an exception for duplicates."""
    with pytest.raises(ValueError):
        alias('name', ('duplicate', 'duplicate'))


def test_useless_alias():
    """Ensures that decorator raises an exception for duplicates."""
    with pytest.raises(ValueError):
        alias('name', ('name',))


def test_raises_for_missing_alias():
    """Ensures that decorator raises an exception for missing alias."""
    with pytest.raises(AttributeError):
        @alias('new_alias', ('first', 'second'))  # noqa: WPS431
        class _HasAliasedProp(object):
            def existing(self):
                return None


def test_raises_for_existing_alias():
    """Ensures that decorator raises an exception for existing alias."""
    with pytest.raises(AttributeError):
        @alias('existing', ('first', 'second'))  # noqa: WPS431
        class _HasAliasedProp(object):
            def existing(self):
                return None

            def first(self):
                return None
