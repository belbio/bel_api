from typing import List, Mapping, Any, MutableMapping
from collections import defaultdict
import datetime

import common.mail

import bel.db.arangodb
from bel import BEL
import bel.utils

from bel.Config import config

import logging
log = logging.getLogger(__name__)

# Custom Typings
Edge = Mapping[str, Any]
Facets = MutableMapping[str, Any]

arangodb_client = bel.db.arangodb.get_client()
edgestore_handle = bel.db.arangodb.get_edgestore_handle(arangodb_client)
belapi_handle = bel.db.arangodb.get_belapi_handle(arangodb_client)


def get_edge(edge_id: str) -> Edge:
    """Get Edge from EdgeStore

    Args:
        edge_id: Edgestore edge._key value

    Return:
        Edge
    """

    query = f"""
    FOR edge IN edges
        FILTER edge._key == '{edge_id}'
        RETURN edge
    """

    edges = bel.db.arangodb.aql_query(edgestore_handle, query)

    for edge in edges:
        return edge


def get_edges(node_query: str = None, hops: int = 1, direction: str = 'ANY', contains: bool = False, filters: Mapping[str, Any] = None, limit: int = 1000, offset: int = 0) -> List[Edge]:
    """Get Edges from EdgeStore

    Args:
        node_query: BEL subject/object or subcomponent
        hops: how many network hops to allow 1=None, 2=one node out, ...
        direction: INBOUND, OUTBOUND, ANY - see ArangoDB docs
        contains: contains node (True) or equals node (False)
            contains node will find all nodes with the canonical node contained in it
        limit: limit to this many edges
        offset: offset to this starting point to return the limit number of edges

    Returns:
        List[Edge]: list of edges (or empty list)
    """
    pass  # TODO
