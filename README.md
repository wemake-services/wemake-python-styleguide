# wemake-python-styleguide

[![wemake.services](https://img.shields.io/badge/-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services)
[![Build Status](https://travis-ci.org/wemake-services/wemake-python-styleguide.svg?branch=master)](https://travis-ci.org/wemake-services/wemake-python-styleguide)
[![Coverage](https://coveralls.io/repos/github/wemake-services/wemake-python-styleguide/badge.svg?branch=master)](https://coveralls.io/github/wemake-services/wemake-python-styleguide?branch=master)
[![PyPI version](https://badge.fury.io/py/wemake-python-styleguide.svg)](https://badge.fury.io/py/wemake-python-styleguide)
[![Documentation Status](https://readthedocs.org/projects/wemake-python-styleguide/badge/?version=latest)](https://wemake-python-styleguide.readthedocs.io/en/latest/?badge=latest)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/wemake-services/wemake-python-styleguide/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)
[![Build status](https://ci.appveyor.com/api/projects/status/github/wemake-python-styleguide?svg=true)](https://ci.appveyor.com/project/sobolevn/wemake-python-styleguide)




Welcome to the most opinionated linter ever.

`wemake-python-styleguide` is actually `flake8` plugin
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


## What does this linter do?

We have several primary objectives with this linter:

0. Enforce `python3.6+` usage
1. Significantly educe code's complexity and make it more maintainable
2. Forbid to use different stuff from `python` language to match
  "There should be one-- and preferably only one --obvious way to do it" rule
3. Create consistent coding style


## What we are not

We are here not to:

1. Assume or check types, use `mypy` instead
2. Reformat code, since we believe that developers should do that
3. Check for `SyntaxError`s or exceptions, write tests instead
4. Suite everyone, this is *our* linter


## Contributing

See [CONTRIBUTING.md](https://github.com/wemake-services/wemake-python-styleguide/blob/master/CONTRIBUTING.md) file if you want to contribute.
You can also check which [issues need some help](https://github.com/wemake-services/wemake-python-styleguide/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) right now.


## License

MIT. See [LICENSE](https://github.com/wemake-services/wemake-python-styleguide/blob/master/LICENSE) for more details.
