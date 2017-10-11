import falcon
import models.es

from Config import config  # Application settings enabled for Dev/Test/Prod

import logging
log = logging.getLogger(__name__)

es = models.es.es


class SimpleStatusResource(object):
    """Simple status - always un-authenticated endpoint"""

    def on_get(self, req, resp):

        resp.context['result'] = {"profile": "Simple Status API Endpoint works"}
        resp.status = falcon.HTTP_200


class StatusResource(object):
    """Status endpoint - authentication may be required


    Returns:
        Mapping(str, Any): Return application settings and database stats
    """

    def on_get(self, req, resp):

        stats = models.es.namespace_term_counts()

        settings = config.dump(config)
        del settings['secrets']
        resp.context['result'] = {"api_settings": settings, 'elasticsearch_stats': stats, 'arangodb_stats': None}

        resp.status = falcon.HTTP_200

        # TODO dump out all configuration except secrets with Status endpoint
