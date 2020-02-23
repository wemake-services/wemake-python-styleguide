#!/usr/bin/env perl
from sys import *
import sys
from typing import List, Union, Dict

int = 12
++int

extra_parens = list((node for node in 'abc'))
some_tuple = (1, 2, )
breaking_pycodestyle=3

# commented: str = 'comment'

def camelCase(): ...

'{}'.format(1)
""
'%s' % 'test'

assert True
ipdb.set_trace()


def function_name(plugin: str ='flake8') ->str:
    """Test `wrong`rst code."""
    return plugin


multiline_string = 'some\
string'

'\''


def darglint_check(arg):
    """
    Used to trigger DAR101.

    Returns:
        Just a value to trigger the check.

    """
    return 'check trigger'
