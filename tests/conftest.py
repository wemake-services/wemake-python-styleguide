# -*- coding: utf-8 -*-

import ast
import os

import pytest
from flake8.processor import FileProcessor


@pytest.fixture(scope='session')
def absolute_path():
    dirname = os.path.dirname(__file__)

    def make_absolute_path(*files):
        return os.path.join(dirname, *files)

    return make_absolute_path
