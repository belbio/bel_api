#!/usr/bin/env bash

# run via: bash <(curl -s https://raw.githubusercontent.com/belbio/bel_api/master/bin/install.sh)
#

hash docker 2>/dev/null || { echo >&2 "I require docker. Please install.  Aborting."; exit 1; }
hash docker-compose 2>/dev/null || { echo >&2 "I require docker-compose. Please install.  Aborting."; exit 1; }


ssh_status=$(ssh -o BatchMode=yes -o ConnectTimeout=5 git@github.com 2>&1)

if [[ $ssh_status == *"successfully authenticated"* ]] ; then
  clone_cmd="git clone git@github.com:belbio/bel_api.git";
else
  clone_cmd="git clone https://github.com/belbio/bel_api.git";
fi

if [ ! -d "bel_api" ]; then
    $clone_cmd
fi

cd bel_api
HOME=$(pwd)

git pull;

if [ ! -f "$HOME/api/Config.yml" ]; then
    cp $HOME/api/Config.yml.sample $HOME/api/Config.yml
    printf "Remember to update api/config.yml\n\n"
fi

echo "Starting to build the docker containers\n\n"
docker-compose build
docker-compose create


echo "To start the docker containers: "
echo "  docker-compose start or docker-compose up\n"

