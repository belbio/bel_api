import elasticsearch
import falcon
from typing import Mapping, Dict, List, Any, Optional, Union, Tuple
import re

from models.es import es
from models.arangodb import arangodb

from services.terms import canonicalize, decanonicalize

import logging
log = logging.getLogger(__name__)

default_canonical_namespace = 'EG'  # for genes, proteins


def get_ortholog(gene_id: str, tax_id: str) -> Optional[str]:
    """Get ortholog

    Args:
        gene_id (str): gene_id for which to retrieve ortholog
        species (str): target species for ortholog

    Returns:
        (str): gene_id of ortholog if available, None otherwise
    """

    gene_id = canonicalize(gene_id)
    query = f'FOR vertex IN 1..1 ANY "ortholog_nodes/{gene_id}" ortholog_edges FILTER vertex.tax_id == "{tax_id}" RETURN vertex._key'
    log.info(query)
    cursor = arangodb.aql.execute(query)

    for record in cursor:
        ortholog = record

    ortholog = decanonicalize(ortholog)
    return ortholog
