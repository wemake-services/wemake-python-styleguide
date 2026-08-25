Command line tool and AI
========================

CLI
---

.. versionadded:: 1.1.0

WPS has a command-line utility named ``wps``

Here are listed all the subcommands it has.

wps explain
~~~~~~~~~~~

This command can be used to get description of violation.
It will be the same description that is located on the website.

Syntax: ``wps explain <code>``

Examples:

.. code:: console

   $ wps explain WPS115
   WPS115 — Require ``snake_case`` for naming class attributes.

   Attributes in Enum and enum-like classes (Django Choices)
   are ignored, as they should be written in UPPER_SNAKE_CASE
   ...

.. code:: console

   $ wps explain 116
   WPS116 — Forbid using more than one consecutive underscore in variable names.

   Reasoning:
       This is done to gain extra readability.
   ...

AI features
-----------

.. versionadded:: 1.8.0

``wemake-python-styleguide`` supports multiple AI features
to help your agent writing the best possible Python code.

We support several different AI features for most of the agents / models.

Skill
~~~~~

Install for any harness / provider,
using `npx skills <https://github.com/vercel-labs/skills>`_:

.. code:: console

  $ npx skills add wemake-services/wemake-python-styleguide

Install with `Claude <https://code.claude.com/docs/en/discover-plugins>`_,
run inside the Claude code:

.. code:: console

  /plugin marketplace add wemake-services/wemake-python-styleguide
  /plugin install wps@wemake-python-styleguide

Or just copy `the skill file <https://github.com/wemake-services/wemake-python-styleguide/blob/master/.agents/skills/wps/SKILL.md>`_.

MCP
~~~

The best way to use our MCP is to use our skill
for your agent, it contains all the information
about installing and starting the MCP server.

This command starts a Model Context Protocol server over standard input and
output. The server exposes an ``explain_violation`` tool that returns the same
description as ``wps explain``.

Install the optional dependency before starting the server:

.. code:: console

   $ pip install 'wemake-python-styleguide[mcp]'

Next, run the server:

.. code:: console

   $ mcp run wemake_python_styleguide/mcp.py:mcp

The MCP SDK command-line tool can also open the server in the MCP Inspector:

.. code:: console

   $ mcp dev wemake_python_styleguide/mcp.py:mcp

These commands use the standard input and output transport, which does not
listen on a network port.
