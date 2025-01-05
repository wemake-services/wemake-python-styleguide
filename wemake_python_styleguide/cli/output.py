"""Provides tool for outputting data."""

from abc import abstractmethod
from typing import Protocol, TextIO


class Writable(Protocol):
    """Interface for outputting text data."""

    @abstractmethod
    def write_out(self, *args) -> None:
        """Write usual text. Works as print."""

    @abstractmethod
    def write_err(self, *args) -> None:
        """Write error text. Works as print."""

    @abstractmethod
    def flush(self) -> None:
        """Flush all outputs."""


class BufferedStreamWriter(Writable):
    """Writes to provided buffered text streams."""

    def __init__(
        self,
        out_stream: TextIO,
        err_stream: TextIO,
        newline_sym: str = '\n'
    ):
        """Create stream writer."""
        self._out = out_stream
        self._err = err_stream
        self._newline = newline_sym.encode()

    def write_out(self, *args) -> None:
        """Write usual text. Works as print."""
        self._out.buffer.write(' '.join(args).encode())
        self._out.buffer.write(self._newline)

    def write_err(self, *args) -> None:
        """Write error text. Works as print."""
        self._err.buffer.write(' '.join(args).encode())
        self._err.buffer.write(self._newline)

    def flush(self) -> None:
        """Flush all outputs."""
        self._out.flush()
        self._err.flush()
