Command line tool and MCP
=========================

.. versionadded:: 1.1.0

WPS has a command-line utility named ``wps``

Here are listed all the subcommands it has.

wps explain
-----------

This command can be used to get description of violation.
It will be the same description that is located on the website.

Syntax: ``wps explain <code>``

Examples:

.. code:: text

   $ wps explain WPS115
   WPS115 — Require ``snake_case`` for naming class attributes.

   Attributes in Enum and enum-like classes (Django Choices)
   are ignored, as they should be written in UPPER_SNAKE_CASE
   ...

.. code:: text

   $ wps explain 116
   WPS116 — Forbid using more than one consecutive underscore in variable names.

   Reasoning:
       This is done to gain extra readability.
   ...

.. rubric:: ``wps mcp``

This command starts a Model Context Protocol server over standard input and
output. The server exposes an ``explain_violation`` tool that returns the same
description as ``wps explain``.

Install the optional dependency before starting the server:

.. code:: console

   $ pip install 'wemake-python-styleguide[mcp]'
   $ wps mcp
