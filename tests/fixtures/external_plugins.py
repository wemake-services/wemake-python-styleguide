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

logger.info(
    'Hello {world}'.format(world='Earth')
)


def function_name(plugin: str ='flake8') ->str:
    """Test `wrong`rst code."""
    return plugin


multiline_string = 'some\
string'

'\''

print('test')


def complex_annotation(
    first: List[Union[List[str], Dict[str, Dict[str, str]]]],
):
    ...


def radon_check(for_data):
    for first in for_data:
        for second in for_data:
            for third in for_data:
                assert first == second == third
