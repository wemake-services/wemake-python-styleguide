"""
This file contains all possible violations for python 3.15+.

It is used for e2e tests.
"""
from typing import MappingProxyType


lazy import json # noqa: WPS482

my_dict = MappingProxyType({'a': 1}) # noqa: WPS483