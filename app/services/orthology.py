from typing import List

import bel.db.arangodb
from services.terms import canonicalize, decanonicalize

import logging
log = logging.getLogger(__name__)

default_canonical_namespace = 'EG'  # for genes, proteins

arangodb_client = bel.db.arangodb.get_client()
belns_db = bel.db.arangodb.get_belns_handle(arangodb_client)


# TODO Refactor to use bel.terms.orthologs.get_orthologs
def get_ortholog(gene_id: str, tax_id: str = None) -> List[str]:
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
    gene_id_key = bel.db.arangodb.arango_id_to_key(gene_id)
    orthologs = []

    # TODO Clean up duplicated code and normalize the output
    if tax_id:
        query = f'FOR vertex IN 1..3 ANY "ortholog_nodes/{gene_id_key}" ortholog_edges FILTER vertex.tax_id == "{tax_id}" RETURN DISTINCT vertex._key'
        cursor = belns_db.aql.execute(query)
        for record in cursor:
            orthologs.append(decanonicalize(record))
    else:
        query = 'FOR vertex IN 1..3 ANY "ortholog_nodes/{0}" ortholog_edges RETURN DISTINCT {{id: vertex._key, species_id: vertex.tax_id}}'.format(gene_id_key)
        cursor = belns_db.aql.execute(query)
        for record in cursor:
            orthologs.append({'id': decanonicalize(record['id']), 'species_id': record['species_id']})

    return orthologs


