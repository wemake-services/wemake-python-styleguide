Extras
------

There are some tools that are out of scope of this linter,
however they are super cool. And should definitely be used!

Things we highly recommend to improve your code quality:

- `mypy <https://github.com/python/mypy>`_ runs type checks on your python code. Finds tons of issues. Makes your code better, improves you as a programmer. You must use, and tell your friends to use it too
- `import-linter <https://import-linter.readthedocs.io>`_ allows you to define application layers and ensure you do not break that contract. Absolutely must have
- `cohesion <https://github.com/mschwager/cohesion>`_ tool to measure code cohesion, works for most of the times. We recommend to use it as a reporting tool
- `vulture <https://github.com/jendrikseipp/vulture>`_ allows you to find unused code. Has some drawbacks, since there is too many magic in python code. But, it is still very useful tool for the refactoring
- `bellybutton <https://github.com/hchasestevens/bellybutton>`_ allows to write linters for custom use-cases. For example, it allows to forbid calling certain (builtins or custom) functions on a per-project bases. No code required, all configuration is written in ``yaml``
