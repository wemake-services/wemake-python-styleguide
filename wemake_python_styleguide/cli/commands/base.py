"""Contains files common for all wps commands."""

from abc import ABC, abstractmethod
from typing import Protocol


class Initialisable(Protocol):
    """Represents a class that can be initialised with kwargs."""

    def __init__(self, **kwargs) -> None: ...


class AbstractCommand[_ArgsT: Initialisable](ABC):
    """ABC for all commands."""

    args_type: type[_ArgsT]

    @abstractmethod
    def run(self, args: _ArgsT) -> int:
        """Run the command."""
        raise NotImplementedError
