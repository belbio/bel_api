from datetime import datetime

import logging
log = logging.getLogger(__name__)


class FalconStatsMiddleware(object):
    """Calculate time required to process request and log it"""

    def __init__(self, debug=False, **kwargs):
        pass

    def process_request(self, req, resp):
        req.context["start_time"] = datetime.now()

    def process_response(self, req, resp, resource, req_succeeded):
        now = datetime.now()
        delta = now - req.context["start_time"]

        log.info(f'Took {delta.total_seconds() * 1000}ms for {req.uri}')  # milliseconds
