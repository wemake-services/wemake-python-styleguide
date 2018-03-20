# -*- coding: utf-8 -*-

from ast import NodeVisitor

from wemake_python_styleguide.errors import BaseStyleViolation
from wemake_python_styleguide.version import __version__


class BaseNodeVisitor(NodeVisitor):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._errors = []

    @property
    def errors(self):
        # TODO: sort errors
        return self._errors

    def add_error(self, error: BaseStyleViolation):
        self._errors.append(error)
