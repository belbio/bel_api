Installation
==============

The recommended way to use the BEL.bio API is to use the docker image. We publish the released BEL.bio API releases as docker images on Dockerhub at `<https://hub.docker.com/r/belbio/bel_api/>`_.


.. include:: configuration.rst

Docker Compose
------------------

.. include:: ../../docker/docker-compose-image.yml
    :code: yaml

Development Installation
--------------------------

Please read :doc:`link_contributing` to understand how to contribute to this project.

1. Fork the bel_api project at https://github.com/belbio/bel_api
2. `git clone <your project fork>`
3. `make dev_install`
4. To make bel python package editable `pip install -e <directory of bel python package>`

