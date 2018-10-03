# -*- coding: utf-8 -*-

"""
This file contains stuff that has too many branches in the source code.
"""

def check_branches_in_function():
    if 1:
        if 2:
            print()
    elif 3:
        try:
            4
        except:
            5
    elif 6:  # error here
        print()


async def async_check_branches_in_function():
    if 1:
        if 2:
            print()
    elif 3:
        try:
            4
        except:
            5
    elif 6:  # error here
        print()
