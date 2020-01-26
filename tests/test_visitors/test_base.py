# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

from wemake_python_styleguide import constants
from wemake_python_styleguide.visitors.base import BaseFilenameVisitor


class _TestingFilenameVisitor(BaseFilenameVisitor):
    def visit_filename(self):
        """Overridden to satisfy abstract base class."""


def test_base_filename_run_do_not_call_visit(default_options):
    """Ensures that `run()` does not call `visit()` method for stdin."""
    instance = _TestingFilenameVisitor(
        default_options,
        filename=constants.STDIN,
    )
    instance.visit_filename = MagicMock()
    instance.run()

    instance.visit_filename.assert_not_called()
