import falcon
import services.orthology as orthology

from Config import config  # Application settings enabled for Dev/Test/Prod

import logging
log = logging.getLogger(__name__)

# Globals
common_species = {'human': 'TAX:9606', 'mouse': 'TAX:10090', 'rat': 'TAX:10116'}


class OrthologResource(object):
    """Orthology endpoint"""

    def on_get(self, req, resp, gene_id=None, species=None):
        """GET orthologs"""

        tax_id = species

        if gene_id is None:
            resp.media = {'title': 'GET Orthologs', 'description': 'Must provide a gene id in path, e.g. /ortholog/HGNC:AKT1/TAX:10090'}
            resp.status = falcon.HTTP_200
            return

        if tax_id is None:
            resp.media = {'title': 'GET Orthologs', 'description': 'Must provide species in path, e.g. /ortholog/HGNC:AKT1/TAX:10090'}
            resp.status = falcon.HTTP_200
            return

        if tax_id in common_species:
            tax_id = common_species[tax_id]

        ortholog = orthology.get_ortholog(gene_id, tax_id)

        resp.media = {'ortholog': ortholog}
        resp.status = falcon.HTTP_200

