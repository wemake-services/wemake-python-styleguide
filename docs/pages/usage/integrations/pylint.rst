pylint
------

We are not related to the ``pylint`` project.
Yes, we know that it is awesome. But, it has some drawbacks:

1. It makes a lot of type assertions. And does it incorrectly.
   Since we use ``mypy`` there is no sense in this feature.
   Without this feature a lot
   of other ``pylint`` features looses its point as well
2. There are less exisitng plugins for ``pylint`` than for ``flake8``
3. It uses custom ``ast`` parser and library, which can be problematic
4. It is not strict enough for us.
   So, we will have to write our own plugin no matter what platform we use

However, it is important to mention
that ``pylint`` is less radical and more classic in its rules.

``wemake-python-styleguide`` and ``pylint`` shares a lot in common.
They are almost compatible with each other.
The difference is in:

- Several minor rules like `class Some(object):` vs `class Some:`
- Error codes
- Python versions, because ``pylint`` covers more versions
- ``wemake-python-styleguide`` is stricter and finds more
  violatons than ``pylint``
