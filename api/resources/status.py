import falcon

import services.terms as terms
from Config import config  # Application settings enabled for Dev/Test/Prod

import logging
log = logging.getLogger(__name__)


class SimpleStatusResource(object):
    """Simple status - always un-authenticated endpoint"""

    def on_get(self, req, resp):

        resp.media = {"profile": "Simple unauthenticated status API endpoint works"}
        resp.status = falcon.HTTP_200


class StatusResource(object):
    """Status endpoint - authentication may be required


    Returns:
        Mapping(str, Any): Return application settings and database stats
    """

    def on_get(self, req, resp):

        stats = terms.namespace_term_counts()

        settings = config.dump(config)
        del settings['secrets']
        resp.media = {
            "api_settings": settings,
            'elasticsearch_stats': stats,
            'arangodb_stats': None
        }

        resp.status = falcon.HTTP_200


class VersionResource(object):
    """Version endpoint"""

    def on_get(self, req, resp):

        resp.media = {'version': config.version}
        resp.status = falcon.HTTP_200

