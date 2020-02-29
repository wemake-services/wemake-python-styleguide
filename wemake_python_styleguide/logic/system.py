# -*- coding: utf-8 -*-

import os


def file_is_executable(filename: str) -> bool:
    """Checks if a file is executable."""
    return os.access(filename, os.X_OK)
