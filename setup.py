#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os

from setuptools import setup


def get_version():
    """Parses main file to find version token."""
    with open('wemake_python_styleguide/version.py') as version_file:
        for line in version_file:
            if line.startswith('__version__'):
                return line.split('=')[-1].strip().replace("'", '')


# Package meta-data.
NAME = 'wemake-python-styleguide'
DESCRIPTION = 'Opinionated styleguide that we use in wemake.services projects'
URL = 'https://github.com/wemake-services/wemake-python-styleguide'
EMAIL = 'mail@sobolevn.me'
AUTHOR = 'Nikita Sobolev'

REQUIRED = [
    'flake8',
]

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as readme:
    long_description = '\n' + readme.read()


setup(
    name=NAME,
    version=get_version(),
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=[
        'wemake_python_styleguide',
    ],
    keywords=[
        'flake8',
        'plugin',
        'wemake.services',
        'styleguide',
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
            'WPS14 = wemake_python_styleguide:WrongNestedChecker',
        ],
    },
    zip_safe=False,
)
