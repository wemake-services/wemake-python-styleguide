# -*- coding: utf-8 -*-

from ast import NodeVisitor
from typing import List

from wemake_python_styleguide.errors.base import BaseStyleViolation
from wemake_python_styleguide.types import ConfigurationOptions


class BaseNodeVisitor(NodeVisitor):
    """
    This class allows to store errors while traversing node tree.

    Attributes:
        options: contains the options objects passed and parsed by `flake8`.
        errors: list of errors for the specific checker.

    """

    options: ConfigurationOptions

    def __init__(self, options: ConfigurationOptions) -> None:
        """Creates new visitor instance."""
        super().__init__()
        self.options = options
        self.errors: List[BaseStyleViolation] = []

    def add_error(self, error: BaseStyleViolation) -> None:
        """Adds error to the visitor."""
        self.errors.append(error)
