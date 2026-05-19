PyCharm
-------

There are two ways to use ``wemake-python-styleguide`` inside
`PyCharm <https://www.jetbrains.com/pycharm/>`_:

1. `Flake8 Support plugin <https://plugins.jetbrains.com/plugin/11563-flake8-support>`_
2. A custom **File Watcher** configured to run ``flake8`` with WPS enabled

The File Watcher approach is useful
when you want real-time feedback on every file save
or when the plugin does not pick up your WPS installation.

Prerequisites
~~~~~~~~~~~~~

Make sure you have ``wemake-python-styleguide`` installed.
We recommend using `uvx <https://pypa.github.io/uvx/>`_:

.. code:: bash

  uvx install --include-deps wemake-python-styleguide

Locate the ``flake8`` executable inside the uvx virtual environment:

.. code:: text

  # Linux / macOS
  ~/.local/uvx/venvs/wemake-python-styleguide/bin/flake8

  # Windows
  C:\Users\<username>\.local\uvx\venvs\wemake-python-styleguide\Scripts\flake8.exe

Setting up a File Watcher
~~~~~~~~~~~~~~~~~~~~~~~~~

1. Open **Settings** (or **Preferences** on macOS).
2. Navigate to **Tools → File Watchers**.
3. Click **+** and choose **<custom>**.
4. Configure the watcher:

   - **Name**: ``wemake-python-styleguide``
   - **File type**: ``Python``
   - **Scope**: ``Project Files``
   - **Program**: path to the ``flake8`` executable from above
   - **Arguments**: ``--select=WPS $FilePath$``
   - **Output paths to refresh**: ``$FilePath$``
   - **Working directory**: ``$ProjectFileDir$``

5. In the **Advanced Options** section enable:

   - **Auto-save edited files to trigger the watcher**
   - **Trigger the watcher on external changes**

6. Click **OK**.

The watcher will run WPS on every save and show violations
directly in the PyCharm editor and in the **Inspections** panel.

Troubleshooting
~~~~~~~~~~~~~~~

If you do not see any violations:

- Make sure the **Program** path points to the ``flake8`` binary
  that has ``wemake-python-styleguide`` installed inside the same environment.
- Try running the same command from the terminal to verify it works.
- Check that your project has a valid ``setup.cfg`` or ``pyproject.toml``
  with WPS configuration.
