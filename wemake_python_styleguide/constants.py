# -*- coding: utf-8 -*-

BAD_FUNCTIONS = frozenset((
    # Code generation:
    'eval',
    'exec',
    'compile',

    # Magic:
    'globals',
    'locals',
    'vars',
    'dir',

    # IO:
    'input',
    'help',

    # Attribute access:
    'hasattr',
    'delattr',

    # Misc:
    'copyright',
))

BAD_MODULE_METADATA_VARIABLES = frozenset((
    '__author__',
    '__all__',
    '__version__',
    '__about__',
))

BAD_VARIABLE_NAMES = frozenset((
    'data',
    'result',
    'results',
    'item',
    'items',
    'value',
    'values',
    'val',
    'vals',
    'var',
    'vars',
    'content',
    'contents',
    'info',
    'handle',
    'handler',
))

NESTED_CLASSES_WHITELIST = frozenset((
    'Meta',
))

NESTED_FUNCTIONS_WHITELIST = frozenset((
    'decorator',
    'factory',
))
