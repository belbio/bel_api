# Development Notes

## Run development tasks

In order to run in the appropriate development environment, you need to run
the following from the top-level directory with the docker-compose.yml file.
This bel_operations docker instance includes all of the python modules needed
for the main bel_api instance as well as additional python development modules
such as py.test


    docker-compose run bel_operations

This will start a docker container with a python environment setup for testing, etc.

You may want to add the following to your .bash_aliases file

    alias belops="docker-compose run bel_operations"

You can now run tests inside the bel_operations instance:

    ./bin/runtests

The bel_operations prompt will look like `api@<container_id>:/app$`

