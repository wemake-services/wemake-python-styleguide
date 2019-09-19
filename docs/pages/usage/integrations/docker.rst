Docker
------

.. image:: https://img.shields.io/docker/pulls/wemakeservices/wemake-python-styleguide.svg
  :alt: Dockerhub
  :target: https://hub.docker.com/r/wemakeservices/wemake-python-styleguide/

.. image:: https://images.microbadger.com/badges/image/wemakeservices/caddy-docker.svg
  :alt: Image size
  :target: https://microbadger.com/images/wemakeservices/wemake-python-styleguide

We have an existing official image on `DockerHub <https://hub.docker.com/r/wemakeservices/wemake-python-styleguide>`_.

Usage
~~~~~

You can can use it like so:

.. code:: bash

  docker pull wemakeservices/wemake-python-styleguide
  docker run --rm wemakeservices/wemake-python-styleguide .

Make sure to place proper config file
and mount it with the source code like so:

.. code:: bash

  docker run --rm wemakeservices/wemake-python-styleguide -v `pwd`:/code /code

You can also use this image with Gitlab CI or any other container-based CIs.

Further reading
~~~~~~~~~~~~~~~

- Official `'docker run' docs <https://docs.docker.com/engine/reference/run/>`_
- Official `GitlabCI docs <https://docs.gitlab.com/ee/ci/>`_
