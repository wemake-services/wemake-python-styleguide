from abc import abstractmethod, ABC

from wemake_python_styleguide.cli.commands.base import AbstractCommand
from wemake_python_styleguide.cli.commands.explain.command import (
    ExplainCommand
)
from wemake_python_styleguide.cli.output import Writable


class Application:
    def __init__(self, writer: Writable):
        self._writer = writer

    def run_explain(self, args) -> int:
        return self._get_command(ExplainCommand).run(args)

    def _get_command(self, command_class: type) -> AbstractCommand:
        return command_class(writer=self._writer)
