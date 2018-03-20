# -*- coding: utf-8 -*-

"""
This file contains all prohibited function calls.
"""

x = input('Input x:')

eval('x / 1')
exec('')
compile('')

z = globals()
y = locals()

vars(z)
dir(y)
