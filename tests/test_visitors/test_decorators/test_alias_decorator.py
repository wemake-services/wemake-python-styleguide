# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.decorators import alias


def test_raises_for_duplicates():
    """Ensures that decorator raises an exception for duplicates."""
    with pytest.raises(ValueError):
        alias('name', ('duplicate', 'duplicate'))
