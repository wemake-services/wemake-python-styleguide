# -*- coding: utf-8 -*-

from ast import Module
from typing import Generator

from wemake_python_styleguide.version import __version__


class BaseChecker(object):
    """Base checker class."""

    name: str
    version = __version__

    def __init__(self, tree: Module, filename: str = '-') -> None:
        """Creates new checker instance."""
        self.tree = tree
        self.filename = filename

    def run(self) -> Generator[tuple, None, None]:
        """
        Runs the checker.

        All subclass must implement this abstract method.
        This method is used by `flake8` API.
        """
        raise NotImplementedError()
