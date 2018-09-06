import falcon
import json

import services.tasks

from bel.Config import config

import structlog
log = structlog.getLogger(__name__)


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
        data = req.media
        resource_url = data.get('resource_url', None)
        forceupdate = data.get('forceupdate', False)

        if not resource_url:
            raise falcon.HTTPBadRequest(
                "No resource_url set",
                "For resource task request, resource_url must be set",
            )

        task_id = services.tasks.add_namespace.delay(resource_url, forceupdate=forceupdate)
        message = "Check the Task Monitor UI for status"
        resp.media = {'title': 'BEL resource task submitted', 'task_id': str(task_id), 'message': message}


class PipelineTasksResource(object):
    """Nanopub -> Edge pipeline tasks endpoint"""

    def on_post(self, req, resp):
        """POST Task - queue Pipeline Tasks"""

        # BEL Pipeline (Nanopub -> Edge conversion)
        start_dt = req.get_param('start_dt', default=None)
        log.info(f'Start_dt: {start_dt}')
        nanopubstore_url = req.get_param('nanopubstore_url', default=config['bel_api']['servers']['nanopubstore'])
        orthologize_targets = req.get_param('orthologize_targets', default=[])

        submitted_cnt = services.tasks.queue_nanopubs(nanopubstore_url, start_dt, orthologize_targets=orthologize_targets)
        log.info(f'Submitted {submitted_cnt} nanopubs to queue')
        if submitted_cnt >= 0:
            message = f"Check the Task Monitor UI for status. Submitted {submitted_cnt} Nanopubs to queue."
            resp.media = {'title': 'Nanopubs queued for BEL Pipeline', 'message': message, 'submitted_cnt': submitted_cnt}
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_400
            resp.media


