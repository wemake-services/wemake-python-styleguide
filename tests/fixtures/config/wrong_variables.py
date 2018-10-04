# -*- coding: utf-8 -*-

"""
This file contains stuff that has too many variables.
"""

def chech_local_variables():
    a1 = '1'
    a2 = '2'
    a3 = '3'
    a4 = '4'
    a5 = '5'
    a6 = '6'
    a7 = '7'
    a8 = '8'
    a9 = '9'
    a10 = '10'  # error here


def check_local_variables_with_single_body():
    with open('some') as context_counts:
        try:
            a1 = '1'
            a2 = '2'
            a3 = '3'
            a4 = '4'
            a5 = '5'
        except Exception as ex_does_not_count:
            a6 = '6'
            a7 = '7'
            a8 = '8'
            a9 = '9'  # error here


async def async_chech_local_variables():
    a1 = '1'
    a2 = '2'
    a3 = '3'
    a4 = '4'
    a5 = '5'
    a6 = '6'
    a7 = '7'
    a8 = '8'
    a9 = '9'
    a10 = '10'  # error here


async def async_check_local_variables_with_single_body():
    with open('some') as context_counts:
        try:
            a1 = '1'
            a2 = '2'
            a3 = '3'
            a4 = '4'
            a5 = '5'
        except Exception as ex_does_not_count:
            a6 = '6'
            a7 = '7'
            a8 = '8'
            a9 = '9'  # error here
