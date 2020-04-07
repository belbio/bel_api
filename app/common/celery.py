import os

from celery import Celery, signals
from kombu import Queue

import bel.setup_logging

CELERY_BROKER = os.environ.get('CELERY_BROKER')
CELERY_BACKEND = os.environ.get('CELERY_BACKEND')

celery_app = Celery('celery',
             broker=CELERY_BROKER,
             backend=CELERY_BACKEND,
             include=['services.tasks'])

# Optional configuration, see the application user guide.
celery_app.conf.update(
    result_expires=3600,
)
celery_app.conf.task_default_queue = 'default'
celery_app.conf.task_queues = (
    Queue('default', routing_key='task.#'),
    Queue('bel_pipeline', routing_key='task.pipeline.#'),
    Queue('bel_resources', routing_key='task.resources.#'),
)


if __name__ == '__main__':
    celery_app.start()
