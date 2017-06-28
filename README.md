# BEL API

The BEL API provides a REST API for the BEL Language and platform services
for using the BEL Language and BEL Content.

Functionality provided:

* BEL language parsing and validation
* BEL Nanopub management and validation
* BEL Edge creation from BEL Nanopubs
* BEL EdgeStore services

## Installation

The following bash command will do the following:

* check for the docker, docker-compose commands
* git clone or git pull depending on if 'bel_api' directory exists
* download the needed datasets from datasets.openbel.org
* provide commands to start the docker containers

    bash <(curl -s https://bitbucket.org/pmiworks/bel_api/raw/HEAD/bin/install.sh)


###  Post install script

Add hostnames to /etc/hosts (unix'ish machines) or /windows/system32/drivers/etc/hosts (Windows)

    127.0.0.1 belapi.test
    127.0.0.1 kibana.belapi.test
    127.0.0.1 swagger_ui.belapi.test
    127.0.0.1 swagger_edit.belapi.test
    127.0.0.1 arangodb.belapi.test
    127.0.0.1 docs.belapi.test

Run following commands to start development:

    cd bel_api
    cp api/Config.yml.sample api/Config.yml
    # Edit Config.yml
    docker-compose start
    docker-compose logs -f


You should now be able to access the following services via your browser:

* API test endpoint:  http://belapi.test/simple-status
* Elasticsearch: http://localhost:9210/
* Kibana: http://kibana.belapi.test/
* Arangodb: http://arangodb.belapi.test/
* Swagger Editor: http://swagger_edit.belapi.test/
* Swagger UI: http://swagger_ui.belapi.test/
* Traefik:  http://localhost:8088/
* API docs: http://docs.belapi.test  (e.g. http://docs.belapi.test/docs/openapi.yaml)

You can enter this url for the Swagger/OpenAPI spec in Swagger UI

    http://docs.belapi.test/docs/openapi.yaml


