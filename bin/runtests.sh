#!/usr/bin/env bash

if [ ! -d "./tests" ]; then
    echo "Need to run this from bel_api top-level directory where ./tests"
    echo "  is a subdirectory"
    exit
fi

py.test -rs --exitfirst --cov=api --cov-report html --cov-config .coveragerc -c tests/pytest.ini --color=yes --durations=10 --flakes --pep8 tests
