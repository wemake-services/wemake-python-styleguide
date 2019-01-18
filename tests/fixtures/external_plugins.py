from sys import *
import sys

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
    return plugin


multiline_string = 'some\
string'

print('test')
