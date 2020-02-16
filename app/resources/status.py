import copy

import falcon
# import logging
import structlog
from bel.Config import config

import services.terms as terms

log = structlog.getLogger(__name__)


class SimpleStatusResource(object):
    """Simple status - always un-authenticated endpoint"""

    def on_get(self, req, resp):

        resp.media = {"message": "Simple unauthenticated status API endpoint works"}
        resp.status = falcon.HTTP_200


class HealthCheckResource(object):
    """Simple healthcheck status - always un-authenticated endpoint"""

    def on_get(self, req, resp):

        resp.media = {
            "message": "Simple unauthenticated health status check",
            "up": True,
        }
        resp.status = falcon.HTTP_200



class PingResource(object):
    """Check service - no authentication/token required"""

    def on_get(self, req, resp):

        resp.media = {"running": True}
        resp.status = falcon.HTTP_200


class StatusResource(object):
    """Status endpoint - authentication may be required


    Returns:
        Mapping(str, Any): Return application settings and database stats
    """

    def on_get(self, req, resp):

        try:
            stats = terms.namespace_term_counts()
        except Exception as e:
            log.info('No term counts: {e}')
            stats = "No elasticsearch index accessible"

        settings = copy.deepcopy(config)
        del settings['secrets']

        versions = get_versions()

        resp.media = {
            'api_version': versions.get('bel_api', 'Unknown'),
            'bel_python_package_version': versions.get('bel_python_package', 'Unknown'),
            "api_settings": settings,
            'elasticsearch_stats': stats,
            'arangodb_stats': 'Not implemented yet',
        }

        resp.status = falcon.HTTP_200


class VersionResource(object):
    """Version endpoint"""

    def on_get(self, req, resp):
        versions = get_versions()
        resp.media = {
            'api_version': versions.get('bel_api', 'Unknown'),
            'bel_python_package': versions.get('bel_python_package', 'Unknown'),
        }
        resp.status = falcon.HTTP_200


def get_versions() -> dict:
    """Get versions of BEL.bio modules and tools"""

    versions = {}
    try:
        import bel.__version__
        versions['bel_python_package'] = bel.__version__.__version__
    except ModuleNotFoundError:
        pass

    try:
        import __version__
        if __version__.__name__ == 'BELBIO API':
            versions['bel_api'] = __version__.__version__
    except ModuleNotFoundError:
        pass

    return versions
