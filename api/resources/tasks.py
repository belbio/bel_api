import json
import logging

import falcon
from bel.Config import config

import services.tasks

log = logging.getLogger(__name__)


class TasksResource(object):
    """Tasks endpoint"""

    def on_get(self, req, resp):
        """Get list of tasks in queue"""

        pass  # TODO - get list of tasks
        # http://docs.celeryproject.org/en/latest/userguide/monitoring.html#inspecting-queues
        # https://stackoverflow.com/questions/17863626/retrieve-queue-length-with-celery-rabbitmq-django/39230080#39230080


class ResourcesTasksResource(object):
    """BEL resources tasks endpoint"""

    def on_post(self, req, resp):
        """POST Task - queue BEL Resource Task
        """

        # Task types
        # bel_pipeline - nanopub to edge conversion
        # add_namespace - load BEL namespace
        # add_orthology - load BEL orthology

        # BEL Resources loading
        data = json.load(req.bounded_stream)
        resource_url = data.get("resource_url", None)

        if not resource_url:
            raise falcon.HTTPBadRequest(
                "No resource_url set", "For resource task request, resource_url must be set"
            )

        task_id = services.tasks.add_namespace.delay(resource_url)
        message = "Check the Task Monitor UI for status"
        resp.media = {
            "title": "BEL resource task submitted",
            "task_id": str(task_id),
            "message": message,
        }
