import sys
from abc import abstractmethod
from typing import Protocol, Unpack, TextIO, AnyStr


class Writable(Protocol):
    @abstractmethod
    def write_out(self, *args: Unpack[AnyStr]) -> None:
        ...

    @abstractmethod
    def write_err(self, *args: Unpack[AnyStr]) -> None:
        ...

    @abstractmethod
    def flush(self) -> None:
        ...


class BufferedStreamWriter(Writable):
    def __init__(
        self,
        out_stream: TextIO,
        err_stream: TextIO,
        newline_sym: str = '\n'
    ):
        self._out = out_stream
        self._err = err_stream
        self._newline = newline_sym.encode()

    def write_out(self, *args: Unpack[AnyStr]) -> None:
        self._out.buffer.write(' '.join(args).encode())
        self._out.buffer.write(self._newline)

    def write_err(self, *args: Unpack[AnyStr]) -> None:
        self._err.buffer.write(' '.join(args).encode())
        self._err.buffer.write(self._newline)

    def flush(self) -> None:
        self._out.flush()
        self._err.flush()
