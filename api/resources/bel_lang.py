import falcon

from bel.lang.belobj import BEL
import bel.lang.bel_specification
import bel.lang.completion
import bel.lang.migrate_1_2
import services.terms as terms

from bel.Config import config

import logging
log = logging.getLogger(__name__)


class BelVersions(object):
    """Get BEL Versions"""

    def on_get(self, req, resp):

        bel_versions = bel.lang.bel_specification.get_bel_versions()
        resp.media = bel_versions
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


class BelCanonicalize(object):
    """Canonicalize BEL"""

    # TODO finish testing and add to Swagger docs

    def on_get(self, req, resp, version, belstr=''):

        namespace_targets = req.get_param('namespace_targets', default=None)
        api_url = config['bel_api']['servers']['api_url']

        log.info(f'Api_url {api_url}')

        bel_obj = BEL(version=version, api_url=api_url)

        canon_belstr = bel_obj.parse(belstr).canonicalize(namespace_targets=namespace_targets).to_string()

        # TODO figure out how to handle naked namespace:val better
        if not canon_belstr:
            canon_belstr = terms.canonicalize(belstr)

        resp.media = {'canonicalized': canon_belstr, 'original': belstr}
        resp.status = falcon.HTTP_200


class BelDecanonicalize(object):
    """Decanonicalize BEL"""

    # TODO finish testing and add to Swagger docs

    def on_get(self, req, resp, version, belstr=''):

        api_url = config['bel_api']['servers']['api_url']
        bel_obj = BEL(version=version, api_url=api_url)

        decanon_belstr = bel_obj.parse(belstr).decanonicalize().to_string()

        resp.media = {'decanonicalized': decanon_belstr, 'original': belstr}
        resp.status = falcon.HTTP_200


class BelMigrate12(object):
    """Migrate BEL1 to BEL2"""

    def on_get(self, req, resp, belstr):

        try:
            belstr = bel.lang.migrate_1_2.migrate(belstr)
        except Exception as e:
            raise falcon.HTTPBadRequest(
                "Cannot migrate",
                "Syntax error - is the provided string valid BEL 1? You may have something like this kin(HGNC:AKT1) which is missing the p() around AKT1.",
            )
        resp.media = {'bel': belstr}
        resp.status = falcon.HTTP_200


class BelSpecificationResource(object):
    """Get BEL Specification enhanced JSON object"""

    def on_get(self, req, resp, version):

        bel_specification = bel.lang.bel_specification.get_specification(version)
        resp.media = bel_specification
        resp.status = falcon.HTTP_200
