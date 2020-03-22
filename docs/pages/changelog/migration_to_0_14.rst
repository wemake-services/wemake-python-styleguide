Migration guide to 0.14
=======================

One of the most important things in this release was
that we are focused on removing extra dependencies.

Why?

For several reasons:

1. Some dependencies do not meet our quality standards:
   there are bugs, lack of recent releases, new language features support, etc

2. Some dependencies are just really simple. Just several lines of code.
   We can simply recreate them inside.
   The good example would be ``flake8-print``,
   we have added just a single configuration line
   to have the very same check internally.

3. Better installation experience. It is faster, less possible conflicts.

Dropped dependencies
--------------------

We have replaced the following dependencies in this release:

- ``flake8-executable`` (check is ported)
- ``flake8-print`` (check is ported)
- ``flake8-builtins`` (check is ported)
- ``flake8-annotations-complexity`` (check is ported)
- ``flake8-pep3101`` (check is ported and modified)
- ``flake8-loggin-format`` (check is dropped)
- ``flake8-coding`` (check is dropped)
- ``radon`` (check is dropped)
- ``cognitive-complexity`` (check is ported)


Changed codes
-------------

When we port a dependency to our own codebase,
this means that we also change the error code.

You would probably have to update it in your source code as well:

- ``EXE001..EXE005`` -> ``WPS452`` (``flake8-executable``)
- ``T001`` -> ``WPS421`` (``flake8-print``)
- ``A001..A005`` -> ``WPS125`` (``flake8-builtins``)
- ``TAE002`` -> ``WPS234`` (``flake8-annotations-complexity``)
- ``S001`` -> ``WPS323`` (``flake8-pep3101``)

You would possibly want to manually install dropped dependencies again.
In case you need them. Or just ignore them (as we do).
