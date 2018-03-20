#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os

from setuptools import setup

# Package meta-data.
NAME = 'wemake-python-styleguide'
DESCRIPTION = 'Warns about redundant arguments'
URL = 'https://github.com/wemake-services/wemake-python-styleguide'
EMAIL = 'mail@sobolevn.me'
AUTHOR = 'Nikita Sobolev'

REQUIRED = [
    'flake8',
]

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


setup(
    name=NAME,
    version='0.0.1',
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    py_modules=['flake8_arguments'],
    keywords=[
        'flake8',
        'plugin',
        'arguments',
        'functions',
        'methods',
    ],
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: Flake8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',

        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],

    entry_points={
        'flake8.extension': [
            'WPS10 = wemake_python_styleguide:WrongKeywordChecker',
            'WPS11 = wemake_python_styleguide:WrongFunctionCallChecker',
            'WPS12 = wemake_python_styleguide:WrongVariableChecker',
            'WPS13 = wemake_python_styleguide:WrongImportChecker',
        ],
    },
    zip_safe=False,
)
