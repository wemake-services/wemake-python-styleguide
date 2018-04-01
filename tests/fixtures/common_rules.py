# -*- coding: utf-8 -*-

"""
This file contains stuff that violates some base rules.
"""

raise  # error here
raise ValueError()

try:
    1 / 0
except Exception:
    raise


class CheckAbstractMethods():
    def check_not_implemented(self):
        raise NotImplemented()  # error here

    def check_not_implemented_without_call(self):
        raise NotImplemented  # error here

    def check_normal(self):
        raise NotImplementedError()
