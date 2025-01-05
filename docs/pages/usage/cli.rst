Command line tool
=================

WPS v1.1.0 introduces new feature: a command-line utility called ``wps``.

.. rubric:: ``wps explain``

This command can be used to get description of violation.
It will be the same description that is located on the website.

Syntax: ``wps explain <code>``

Examples:

.. code::
   $ wps explain WPS115
   WPS115 (UpperCaseAttributeViolation)

   WPS115 - Require ``snake_case`` for naming class attributes.
   ...

.. code::
   $ wps explain 116
   WPS116 (ConsecutiveUnderscoresInNameViolation)

   WPS116 - Forbid using more than one consecutive underscore in variable names.



.. versionadded:: 1.1.0
