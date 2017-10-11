#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:  program.py <customer>

"""

from arango import ArangoClient, ArangoError
from typing import Mapping, Dict, List, Any, Optional, Union, Tuple
import logging

log = logging.getLogger(__name__)

client = ArangoClient(
    protocol='http',
    host='localhost',
    port=8529,
    username='',
    password='',
    enable_logging=True,
)

db_name = 'bel'
ortholog_node_coll_name = 'ortholog_nodes'
ortholog_edge_coll_name = 'ortholog_edges'
equiv_node_coll_name = 'equivalence_nodes'
equiv_edge_coll_name = 'equivalence_edges'


def get_equivalences(equivalences: Mapping[str, Any]) -> Mapping[str, Any]:
    """Get equivalences given ns:id and target namespaces

    The target_namespaces list in the argument dictionary is ordered by priority.

    Args:
        equivalences (Mapping[str, Any]): e.g. {'id': 'HGNC:5', target_namespaces: ['EG', 'SP']}

    Returns:
        Mapping[str, Any]: e.g. {'id': 'HGNC:5', 'equivalent': 'EG:1'}
    """

# ### Get namespace equivalence

#     FOR vertex, edge
#     IN 1..10
#     ANY "equivalence_nodes/HGNC:A1BG" equivalence_edges
#     FILTER vertex.namespace == "SP"  # probably need to do this in the function
#     RETURN vertex._key
