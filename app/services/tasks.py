import datetime
from time import sleep
from typing import List

import bel.edge.edges
import bel.resources.resource
import bel.utils
import structlog

from common.celery import celery_app

log = structlog.getLogger(__name__)


@celery_app.task
def add_namespace(resource_url):
    """Add BEL resource_url to bel_resources queue"""

    bel.resources.resource.load_resource(resource_url)
