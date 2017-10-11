import falcon
import models.es

from Config import config  # Application settings enabled for Dev/Test/Prod

import logging
log = logging.getLogger(__name__)

es = models.es.es


class TermResource(object):
    """User Profile"""

    def on_get(self, req, resp, term_id):
        """GET User Profile"""

        pass

    def on_put(self, req, resp, profile):
        """Update User Profile"""
        pass

    def on_delete(self, req, resp, userid):
        """DELETE User"""
        pass


class TermsResource(object):

    """Get Users listing based on query - generally by organization

    create new
    """

    def on_get(self, req, resp, query, start, pagesize):
        """GET List of Terms
            Args:
                query (str): query string for terms
                start (int): start page
                pagesize (int): number of users per page
            Results:
                List[Mapping[str, Any]]: list of users
        """
        pass

    def on_post(self, req, resp):
        """Create User

        """
        pass
