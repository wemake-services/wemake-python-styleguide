# -*- coding: utf-8 -*-

"""
This is the script you can use to see the tokens contents of a python module.

Usage:

.. code:: python

    python ./scripts/tokens.py my_test_module.py

"""

import io
import sys
import tokenize


def _main(filename: str) -> None:
    with open(filename) as file_to_read:
        file_contents = file_to_read.read()

    lines = io.StringIO(file_contents)
    for token in tokenize.generate_tokens(lambda: next(lines)):
        print(token)  # noqa: T001


if __name__ == '__main__':
    _main(sys.argv[1])
