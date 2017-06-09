#!/usr/bin/env bash

# run via: bash <(curl -s https://bitbucket.org/pmiworks/bel_api/raw/HEAD/bin/install.sh)

hash docker 2>/dev/null || { echo >&2 "I require docker. Please install.  Aborting."; exit 1; }
hash docker-compose 2>/dev/null || { echo >&2 "I require docker-compose. Please install.  Aborting."; exit 1; }


ssh_status=$(ssh -o BatchMode=yes -o ConnectTimeout=5 git@bitbucket.com 2>&1)

if [[ $ssh_status == *"successfully authenticated"* ]] ; then
  clone_cmd="git clone git@bitbucket.org:pmiworks/bel_api.git";
else
  clone_cmd="git clone https://wshayes@bitbucket.org/pmiworks/bel_api.git";
fi

if [ ! -d "bel_api" ]; then
    $clone_cmd
else
    cd bel_api;
    git pull;
    cd ..;
fi

cd bel_api
HOME=$(pwd)

if [ ! -f "$HOME/config.yml" ]; then
    cp config.yml.example config.yml
fi

printf "Remember to update config.yml\n\n"

echo "To start the docker containers: "
echo "  docker-compose build"
echo "  docker-compose up"

printf "\n\nTo run production docker: "
echo "  docker-compose -f docker-compose-prod.yml build"
echo "  docker-compose -f docker-compose-prod.yml up"

