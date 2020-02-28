# wemake-python-styleguide

[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services)
[![Supporters](https://img.shields.io/opencollective/all/wemake-python-styleguide.svg?color=gold&label=supporters)](https://opencollective.com/wemake-python-styleguide)
[![Build Status](https://travis-ci.com/wemake-services/wemake-python-styleguide.svg?branch=master)](https://travis-ci.com/wemake-services/wemake-python-styleguide)
[![Coverage Status](https://coveralls.io/repos/github/wemake-services/wemake-python-styleguide/badge.svg?branch=master)](https://coveralls.io/github/wemake-services/wemake-python-styleguide?branch=master)
[![Python Version](https://img.shields.io/pypi/pyversions/wemake-python-styleguide.svg)](https://pypi.org/project/wemake-python-styleguide/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

---

Welcome to the strictest and most opinionated python linter ever.

<p align="center">
  <a href="https://wemake-python-stylegui.de">
    <img src="https://raw.githubusercontent.com/wemake-services/wemake-python-styleguide/master/docs/_static/logo.png"
         alt="wemake-python-styleguide logo">
  </a>
</p>

`wemake-python-styleguide` is actually a [flake8](http://flake8.pycqa.org/en/latest/)
plugin with [some other plugins](https://wemake-python-stylegui.de/en/latest/pages/usage/violations/index.html#external-plugins) as dependencies.


## Quickstart

```bash
pip install wemake-python-styleguide
```

You will also need to create a `setup.cfg` file with the [configuration](https://wemake-python-stylegui.de/en/latest/pages/usage/configuration.html).

We highly recommend to also use:

- [flakehell](https://wemake-python-stylegui.de/en/latest/pages/usage/integrations/flakehell.html) for easy integration into a **legacy** codebase
- [nitpick](https://wemake-python-stylegui.de/en/latest/pages/usage/integrations/nitpick.html) for sharing and validating configuration across multiple projects


## Running

```bash
flake8 your_module.py
```

This app is still just good old `flake8`!
And it won't change your existing workflow.

<p align="center">
  <img src="https://raw.githubusercontent.com/wemake-services/wemake-python-styleguide/master/docs/_static/running.png"
       alt="invocation resuts">
</p>

See ["Usage" section](https://wemake-python-stylegui.de/en/latest/pages/usage/setup.html)
in the docs for examples and integrations.

We also support [Github Actions](https://wemake-python-stylegui.de/en/latest/pages/usage/integrations/github-actions.html) as first class-citizens.
[Try it out](https://github.com/marketplace/actions/wemake-python-styleguide)!


## What we are about

The ultimate goal of this project is
to make all people write **exactly** the same `python` code.

|                            | flake8 | pylint | black | mypy | wemake-python-styleguide |
|----------------------------|--------|--------|-------|------|--------------------------|
| Formats code?              |   ❌   |   ❌   |   ✅  |  ❌  |            ❌           |
| Finds style issues?        |   🤔   |   ✅   |   🤔  |  ❌  |            ✅           |
| Finds bugs?                |   🤔   |   ✅   |   ❌  |  ✅  |            ✅           |
| Finds complex code?        |   ❌   |   🤔   |   ❌  |  ❌  |            ✅           |
| Has a lot of strict rules? |   ❌   |   🤔   |   ❌  |  ❌  |            ✅           |
| Has a lot of plugins?      |   ✅   |   ❌   |   ❌  |  🤔  |            ✅           |

We have several primary objectives:

0. Enforce `python3.6+` usage
1. Significantly reduce complexity of your code and make it more maintainable
2. Enforce "There should be one -- and preferably only one -- obvious way to do it" rule to coding and naming styles
3. Protect developers from possible errors and enforce best practices

You can find all error codes and plugins [in the docs](https://wemake-python-stylegui.de/en/latest/pages/usage/violations/index.html).


## What we are not

We are *not* planning to do the following things:

0. Assume or check types, use `mypy` together with our linter
1. [Reformat code](https://wemake-python-stylegui.de/en/latest/pages/usage/integrations/auto-formatters.html), since we believe that developers should do that
2. Check for `SyntaxError` or logical bugs, write tests instead
3. Appeal to everyone. But, you can [switch off](https://wemake-python-stylegui.de/en/latest/pages/usage/setup.html#ignoring-violations) any rules that you don't like


## Supporting us :tada:

We in [wemake.services](https://wemake.services) make
all our tools open-source by default, so the community can benefit from them.
If you use our tools and they make your life easier and brings business value,
you can return us a favor by supporting the work we do.

[![Gold Tier](https://opencollective.com/wemake-python-styleguide/tiers/gold-sponsor.svg?width=890)](https://opencollective.com/wemake-python-styleguide)

[![Silver Tier](https://opencollective.com/wemake-python-styleguide/tiers/silver-sponsor.svg?width=890&avatarHeight=45&button=0)](https://opencollective.com/wemake-python-styleguide)

[![Bronze Tier](https://opencollective.com/wemake-python-styleguide/tiers/bronze-sponsor.svg?width=890&avatarHeight=35&button=0)](https://opencollective.com/wemake-python-styleguide)


## Show your style :sunglasses:

If you use our linter - it means that your code is awesome.
You can be proud of it!
And you should share your accomplishment with others
by including a badge to your `README` file. It looks like this:

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

### Markdown

```md
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
```

### Restructured text

```rst
.. image:: https://img.shields.io/badge/style-wemake-000000.svg
   :target: https://github.com/wemake-services/wemake-python-styleguide
```


## Contributing

We **warmly welcome** all contributions!

[![List of contributors](https://opencollective.com/wemake-python-styleguide/contributors.svg?width=890&button=0)](https://github.com/wemake-services/wemake-python-styleguide/graphs/contributors)

See ["Contributing"](https://wemake-python-stylegui.de/en/latest/pages/api/index.html#contributing) section in the documentation if you want to contribute.

You can start with [issues that need some help](https://github.com/wemake-services/wemake-python-styleguide/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22)
right now.
