from abc import ABC, abstractmethod

from wemake_python_styleguide.cli.output import Writable


class AbstractCommand(ABC):
    def __init__(self, writer: Writable):
        self.writer = writer

    @abstractmethod
    def run(self, args) -> int:
        ...
