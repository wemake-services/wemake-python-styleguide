# wemake-python-styleguide

[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services)
[![Python Version](https://img.shields.io/pypi/pyversions/wemake-python-styleguide.svg)](https://pypi.org/project/wemake-python-styleguide/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

[![Build Status](https://travis-ci.org/wemake-services/wemake-python-styleguide.svg?branch=master)](https://travis-ci.org/wemake-services/wemake-python-styleguide) 
[![Coverage](https://coveralls.io/repos/github/wemake-services/wemake-python-styleguide/badge.svg?branch=master)](https://coveralls.io/github/wemake-services/wemake-python-styleguide?branch=master)
[![Documentation Status](https://readthedocs.org/projects/wemake-python-styleguide/badge/?version=latest)](https://wemake-python-styleguide.readthedocs.io/en/latest/?badge=latest)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/wemake-services/wemake-python-styleguide/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/wemake-services/wemake-python-styleguide.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/wemake-services/wemake-python-styleguide/context:python)
---

Welcome to the strictest and most opinionated python linter ever.

`wemake-python-styleguide` is actually a `flake8` plugin
with some other plugins as dependencies.

```text
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one-- obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```

## Installation

```bash
pip install wemake-python-styleguide
```

You will also need to create a `setup.cfg` file with [the following contents](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/options/config.html#plugins).

This file is required to configure our linter and all 3rd party plugins it uses.
However, this is a temporary solution.
We are working at providing the required configuration for you in the future.

Running:

```bash
flake8 your_module.py
```

This app is still just good old `flake8`!
And it won't change your existing workflow.

See ["Usage" section](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/setup.html)
in the docs for examples and integrations.


## What we are about

We have several primary objectives:

0. Enforce `python3.6+` usage
1. Significantly reduce complexity of your code and make it more maintainable
2. Enforce "There should be one-- and preferably only one --obvious way to do it" rule to coding and naming styles
3. Protect developers from possible errors and enforce best practices

You can find all error codes and plugins [in the docs](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/violations/index.html).


## What we are not

We are *not* planning to do the following things:

0. Assume or check types, use `mypy` instead
1. Reformat code, since we believe that developers should do that
2. Check for `SyntaxError` or exceptions, write tests instead
3. Appeal to everyone, this is **our** linter. But, you can [switch off](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/setup.html#ignoring-violations) any rules that you don't like


## Show your style

If you use our linter - it means that your code is awesome.
You can be proud of it!
And you should share your accomplishment with others
by including a badge to your `README` file.

It looks like this:

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

### Markdown

```
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
```

### Restructured text

```
.. image:: https://img.shields.io/badge/style-wemake-000000.svg
    :target: https://github.com/wemake-services/wemake-python-styleguide
```


## Contributing

We warmly welcome all contributions!

See ["Contributing"](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/contributing.html)
section in the documentation if you want to contribute.
You can start with [issues that need some help](https://github.com/wemake-services/wemake-python-styleguide/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) right now.
