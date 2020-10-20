# -*- coding: utf-8 -*-

import os

from wemake_python_styleguide.constants import WINDOWS_OS


def is_executable_file(filename: str) -> bool:
    """Checks if a file is executable."""
    return os.access(filename, os.X_OK)


def is_windows() -> bool:
    """Checks if we are running on Windows."""
    return os.name == WINDOWS_OS
