# wemake-python-styleguide

[![wemake.services](https://img.shields.io/badge/-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services)
[![Build Status](https://travis-ci.org/wemake-services/wemake-python-styleguide.svg?branch=master)](https://travis-ci.org/wemake-services/wemake-python-styleguide) [![Build status](https://ci.appveyor.com/api/projects/status/mpopx4wpfkrhc1sl?svg=true)](https://ci.appveyor.com/project/wemake-services/wemake-python-styleguide)
[![Coverage](https://coveralls.io/repos/github/wemake-services/wemake-python-styleguide/badge.svg?branch=master)](https://coveralls.io/github/wemake-services/wemake-python-styleguide?branch=master)
[![Python Version](https://img.shields.io/pypi/pyversions/wemake-python-styleguide.svg)](https://pypi.org/project/wemake-python-styleguide/)
[![Documentation Status](https://readthedocs.org/projects/wemake-python-styleguide/badge/?version=latest)](https://wemake-python-styleguide.readthedocs.io/en/latest/?badge=latest)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/wemake-services/wemake-python-styleguide/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

---

Welcome to the most opinionated linter ever.

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
There should be one-- and preferably only one --obvious way to do it.
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

You will also need to create a `setup.cfg` file with [the following contents](https://wemake-python-styleguide.readthedocs.io/en/latest/_pages/options/config.html#third-party-plugins).

This file is required to configure our linter and 3rd party plugins it uses.
However, this is a temporary solution.
We are working at providing the required configuration for you in the future.

See ["Usage" section](https://wemake-python-styleguide.readthedocs.io/en/latest/_pages/usage.html)
in the docs for examples and integrations.


## What we are about

We have several primary objectives:

0. Enforce `python3.6+` usage
1. Significantly reduce complexity of your code and make it more maintainable
2. Enforce "There should be one-- and preferably only one --obvious way to do it" rule
3. Create consistent coding and naming style

You can find all error codes and plugins [in the docs](https://wemake-python-styleguide.readthedocs.io/en/latest/_pages/violations/index.html).


## What we are not

We are *not* planning to do the following things:

0. Assume or check types, use `mypy` instead
1. Reformat code, since we believe that developers should do that
2. Check for `SyntaxError` or exceptions, write tests instead
3. Appeal to everyone, this is **our** linter


## Contributing

See ["Contributing" section](https://wemake-python-styleguide.readthedocs.io/en/latest/_pages/contributing.html) in the documentation if you want to contribute.
You can also check which [issues need some help](https://github.com/wemake-services/wemake-python-styleguide/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) right now.


## License

MIT. See [LICENSE](https://github.com/wemake-services/wemake-python-styleguide/blob/master/LICENSE) for more details.
