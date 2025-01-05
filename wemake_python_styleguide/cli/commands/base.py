"""Contains files common for all wps commands."""

from abc import ABC, abstractmethod

from wemake_python_styleguide.cli.output import Writable


class AbstractCommand(ABC):
    """ABC for all commands."""

    def __init__(self, writer: Writable):
        """Create a command and define its writer."""
        self.writer = writer

    @abstractmethod
    def run(self, args) -> int:
        """Run the command."""
        raise NotImplementedError
