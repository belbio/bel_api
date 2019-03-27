# Development Notes

## Developing

After going through the setup. You will be able to edit the bel and belapi code and see
the changes made to the docker containers immediately. The belapi code is volume mounted
into the /app directory of the docker container. The bel code is volume mounted into the
python 3.6 package location for the install bel package.

## Setup

To get started:

    bash <(curl -s https://raw.githubusercontent.com/belbio/bel_api/master/bin/setup_dev.sh)

Review configuration in the .env file and the conf directory files

Run:

    docker-compose up -d

## Docker info

    # Follows logs for the belapi service
    docker-compose logs -f bb_belapi

Services:
    bb_belapi - provides BEL API endpoint
    bb_elasticsearch - used for terminology searches/term completion
    bb_arangodb - [graph] database for terms, orthologies, etc
    bb_celery_worker - queue/batch processing manager
    bb_flower - Web GUI for celery
    bb_rabbitmq - Message broker used for queues by celery
    bb_traefik - reverse proxy to provide access to the docker services

## Misc

This will start docker containers needed to run everything.

To make life easier on Macs using local DNS dev domains: https://medium.com/@williamhayes/local-dev-on-docker-fun-with-dns-85ca7d701f0a



