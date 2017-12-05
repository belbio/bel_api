import falcon
import copy

from bel_lang.Config import config
import services.terms as terms

import logging
log = logging.getLogger(__name__)


class SimpleStatusResource(object):
    """Simple status - always un-authenticated endpoint"""

    def on_get(self, req, resp):

        resp.media = {"message": "Simple unauthenticated status API endpoint works"}
        resp.status = falcon.HTTP_200


class StatusResource(object):
    """Status endpoint - authentication may be required


    Returns:
        Mapping(str, Any): Return application settings and database stats
    """

    def on_get(self, req, resp):

        stats = terms.namespace_term_counts()

        settings = copy.deepcopy(config)
        del settings['bel_resources']
        del settings['secrets']

        resp.media = {
            'api_version': config['bel_api'].get('version', 'Unknown'),
            "api_settings": settings,
            'elasticsearch_stats': stats,
            'arangodb_stats': None
        }

        resp.status = falcon.HTTP_200


class VersionResource(object):
    """Version endpoint"""

    def on_get(self, req, resp):

        resp.media = {
            'api_version': config['bel_api'].get('version', 'Unknown'),
            'bel_lang_version': config['bel_lang'].get('version', 'Unknown'),
            'bel_nanopub_version': config['bel_nanopub'].get('version', 'Unknown'),
        }
        resp.status = falcon.HTTP_200

