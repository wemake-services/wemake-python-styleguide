# -*- coding: utf-8 -*-

from ast import NodeVisitor
from typing import List

from wemake_python_styleguide.errors import BaseStyleViolation


class BaseNodeVisitor(NodeVisitor):
    """This class allows to store errors while traversing node tree."""

    def __init__(self) -> None:
        """Creates new visitor instance."""
        super().__init__()
        self._errors: List[BaseStyleViolation] = []

    @property
    def errors(self) -> List[BaseStyleViolation]:
        """Return errors collected by this visitor."""
        return self._errors

    def add_error(self, error: BaseStyleViolation) -> None:
        """Adds error to the visitor."""
        self._errors.append(error)
