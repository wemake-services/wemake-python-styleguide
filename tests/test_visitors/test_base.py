# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

import pytest

from wemake_python_styleguide import constants
from wemake_python_styleguide.visitors.base import (
    BaseChecker,
    BaseFilenameVisitor,
    BaseNodeVisitor,
)


def test_raises_value_error_without_tree(default_options):
    """Ensures that ValueError is raised when visitor does not have a tree."""
    with pytest.raises(ValueError):
        BaseNodeVisitor(default_options).run()


def test_checker_raises_not_implemented(default_options):
    """Ensures that `BaseChecker` raises `NotImplementedError`."""
    with pytest.raises(NotImplementedError):
        BaseChecker(default_options).run()


def test_base_filename_raises_not_implemented(default_options):
    """Ensures that `BaseFilenameVisitor` raises `NotImplementedError`."""
    with pytest.raises(NotImplementedError):
        BaseFilenameVisitor(default_options, filename='some.py').run()


def test_base_filename_run_do_not_call_visit(default_options):
    """Ensures that `run()` does not call `visit()` method for stdin."""
    instance = BaseFilenameVisitor(default_options, filename=constants.STDIN)
    instance.visit_filename = MagicMock()
    instance.run()

    instance.visit_filename.assert_not_called()
