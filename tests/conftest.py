# -*- coding: utf-8 -*-

import os

import pytest


def _make_absolute_path(*files):
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, *files)


@pytest.fixture(scope='session')
def absolute_path():
    """Fixture to create full path relative to `contest.py` inside tests."""
    return _make_absolute_path
