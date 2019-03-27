#!/usr/bin/env bash

URLROOT=https://raw.githubusercontent.com/belbio/bel_api/master

# Create directories
mkdir conf
mkdir bel_specifications

# Clone repos
git clone git@github.com:belbio/bel_api.git belapi
git clone git@github.com:belbio/bel.git

# Set up configuration
curl ${URLROOT}/conf/dotenv.sample -o .env
curl ${URLROOT}/conf/belbio_conf.yml.sample -o conf/belbio_conf.yml
curl ${URLROOT}/conf/belbio_secrets.yml.sample -o conf/belbio_secrets.yml
curl ${URLROOT}/conf/elasticsearch.yml -o conf/elasticsearch.yml
touch conf/belbio_secrets.yml

curl ${URLROOT}/docker-compose.dev.yml -o docker-compose.yml

docker network create belbio

echo "Run following command to start belapi"
echo "  docker-compose up -d"

