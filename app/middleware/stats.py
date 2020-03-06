from datetime import datetime

import structlog
log = structlog.getLogger(__name__)


class FalconStatsMiddleware(object):
    """Calculate time required to process request and log it"""

    def __init__(self, debug=False, **kwargs):
        pass

    def process_request(self, req, resp):
        req.context["start_time"] = datetime.now()

    def process_response(self, req, resp, resource, req_succeeded):
        now = datetime.now()
        delta = now - req.context["start_time"]

        # log.info(f'Took {delta.total_seconds() * 1000}ms for {req.uri}', {"type": "api_request", 'timespan_seconds': delta.total_seconds(), 'uri': req.uri, 'status': resp.status})
        timespan_ms = delta.total_seconds() * 1000  # converted to milliseconds
        type_ = 'api_request'
        if 'healthcheck' in req.uri:
            type_ = 'healthcheck'

        log.info(f'Took {timespan_ms}ms for {req.uri}', type=type_, timespan_ms=timespan_ms, url=req.uri, status=resp.status)



