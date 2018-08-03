import os
import multiprocessing
import logging
# import bel.lang.bel_specification

logger = logging.getLogger(__name__)

worker_class = "gevent"
workers = multiprocessing.cpu_count() * 2 + 1

if os.getenv('BELBIO_SERVER_MODE') == 'DEV':
    workers = 3
    reload = True
    reload_extra_files = ['/belbio/belbio_conf.yml']
else:
    preload_app = True


# https://sebest.github.io/post/protips-using-gunicorn-inside-a-docker-image/

# This code will iterate over all environment variables and find those
# starting by GUNICORN_ and set a local variable with the remaining part,
# lowercased: GUNICORN_MY_PARAMETER=42 will create a variable named
# my_parameter with ‘42’ as the value.
# $ export GUNICORN_WORKERS=2
# $ export GUNICORN_BACKLOG=4096
# $ export GUNICORN_BIND=0.0.0.0:8080

for k, v in os.environ.items():
    if k.startswith("GUNICORN_"):
        key = k.split('_', 1)[1].lower()
        locals()[key] = v

