# -*- coding: utf-8 -*-

"""
This is the script you can use to see the AST contents of a python module.

Usage:

.. code:: python

    python ./scripts/parse.py my_test_module.py

"""

import ast
import sys


def _main(filename: str) -> None:
    with open(filename) as file_to_read:
        file_contents = file_to_read.read()

    for node in ast.walk(ast.parse(file_contents)):
        print(ast.dump(node, include_attributes=True))  # noqa: T001
        print()  # noqa: T001


if __name__ == '__main__':
    _main(sys.argv[1])
