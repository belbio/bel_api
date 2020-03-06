import falcon

import services.pubmed

import logging
log = logging.getLogger(__name__)


class PubmedResource(object):
    """Get """

    def on_get(self, req, resp, pmid):

        pubmed_only_flag = req.get_param('pubmed_only')
        pubmed = services.pubmed.get_pubmed_for_beleditor(pmid, pubmed_only_flag)
        resp.media = pubmed
        resp.status = falcon.HTTP_200
