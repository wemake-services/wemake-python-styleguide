# -*- coding: utf-8 -*-

from ast import Module

from wemake_python_styleguide.version import __version__


class BaseChecker(object):
    name: str
    version = __version__

    def __init__(self, tree: Module, filename: str = '-') -> None:
        self.tree = tree
        self.filename = filename

    def run(self):
        raise NotImplementedError()
