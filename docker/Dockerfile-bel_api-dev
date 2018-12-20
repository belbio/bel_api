FROM python:3.6
MAINTAINER  William Hayes whayes@openbel.org

EXPOSE 8000

RUN pip3 install pipenv

RUN groupadd -g 1000 api && useradd api -u 1000 -g 1000 && mkdir /app && chown -R api:api /app

WORKDIR /app

# -- Adding Pipfiles
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# -- Install dependencies:
RUN set -ex && pipenv install --deploy --system

USER api

# Volume mount ./api directory to /app in docker-compose file for development

# HEALTHCHECK CMD curl --fail http://localhost:8000/healthcheck || exit 1

# https://sebest.github.io/post/protips-using-gunicorn-inside-a-docker-image/
CMD gunicorn --config /app/gunicorn_conf.py --log-config /app/gunicorn_log.conf -b 0.0.0.0:8000 app:api
