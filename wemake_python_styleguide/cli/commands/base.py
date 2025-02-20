"""Contains files common for all wps commands."""

from abc import ABC, abstractmethod
from argparse import Namespace
from typing import Generic, TypeVar

_ArgsT = TypeVar('_ArgsT')


class AbstractCommand(ABC, Generic[_ArgsT]):
    """ABC for all commands."""

    _args_type: type[_ArgsT]

    def __call__(self, args: Namespace) -> int:
        """Parse arguments into the generic namespace."""
        args_dict = vars(args)  # noqa: WPS421
        args_dict.pop('func')  # argument classes do not expect that
        cmd_args = self._args_type(**args_dict)
        return self._run(cmd_args)

    @abstractmethod
    def _run(self, args: _ArgsT) -> int:
        """Run the command."""
        raise NotImplementedError
