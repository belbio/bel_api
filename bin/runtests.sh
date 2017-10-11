#!/usr/bin/env bash

cd api
py.test -rs --exitfirst --cov=. --cov-report html --cov-config .coveragerc -c tests/pytest.ini --color=yes --durations=10 --flakes --pep8 tests
