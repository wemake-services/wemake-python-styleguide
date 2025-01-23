"""Contains files common for all wps commands."""

from abc import ABC, abstractmethod


class AbstractCommand(ABC):
    """ABC for all commands."""

    @abstractmethod
    def run(self, args) -> int:
        """Run the command."""
        raise NotImplementedError
