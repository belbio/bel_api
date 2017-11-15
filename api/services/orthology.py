from typing import List

from models.arangodb import arangodb, arango_id_to_key
from services.terms import canonicalize, decanonicalize

import logging
log = logging.getLogger(__name__)

default_canonical_namespace = 'EG'  # for genes, proteins


def get_ortholog(gene_id: str, tax_id: str) -> List[str]:
    """Get orthologs for given gene_id and species

    Canonicalize prior to ortholog query and decanonicalize
    the resulting ortholog

    Args:
        gene_id (str): gene_id for which to retrieve ortholog
        species (str): target species for ortholog

    Returns:
        List[str]: decanonicalized ortholog IDs if available, None otherwise
    """

    gene_id = canonicalize(gene_id)
    gene_id = arango_id_to_key(gene_id)

    query = f'FOR vertex IN 1..1 ANY "ortholog_nodes/{gene_id}" ortholog_edges FILTER vertex.tax_id == "{tax_id}" RETURN vertex._key'
    log.info(query)
    cursor = arangodb.aql.execute(query)

    orthologs = []
    for record in cursor:
        orthologs.append(decanonicalize(record))

    return orthologs
