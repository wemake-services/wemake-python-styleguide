# -*- coding: utf-8 -*-

import os


def is_executable_file(filename: str) -> bool:
    """Checks if a file is executable."""
    return os.access(filename, os.X_OK)
