import falcon

import bel.lang.bel_specification
import bel.lang.completion

import logging
log = logging.getLogger(__name__)


class BelVersions(object):
    """Get BEL Versions"""

    def on_get(self, req, resp):

        bel_versions = bel.lang.bel_specification.get_bel_versions()
        resp.media = bel_versions
        resp.status = falcon.HTTP_200


class BelSpecificationResource(object):
    """Get BEL Specification enhanced JSON object"""

    def on_get(self, req, resp, version):

        bel_specification = bel.lang.bel_specification.get_specification(version)
        resp.media = bel_specification
        resp.status = falcon.HTTP_200


class BelCompletion(object):
    """Get BEL Completion"""

    def on_get(self, req, resp, version, belstr=''):

        cursor_loc = int(req.get_param('cursor_loc', default=-1))
        bel_comp = req.get_param('bel_comp', default=None)
        bel_fmt = req.get_param('bel_fmt', default='medium')
        species_id = req.get_param('species_id', default=None)

        completions = bel.lang.completion.bel_completion(
            belstr, cursor_loc=cursor_loc, bel_version=version,
            bel_comp=bel_comp, bel_fmt=bel_fmt, species_id=species_id)

        resp.media = completions
        resp.status = falcon.HTTP_200
