#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:  program.py <customer>

"""

from arango import ArangoClient, ArangoError
from typing import Mapping, Dict, List, Any, Optional, Union, Tuple
import logging

from Config import config

log = logging.getLogger(__name__)

arango_client = ArangoClient(
    protocol=config.servers.arangodb_protocol,
    host=config.servers.arangodb_host,
    port=config.servers.arangodb_port,
    username=config.servers.arangodb_username,
    password=config.servers.arangodb_password,
    enable_logging=True,
)

db_name = 'bel'
arangodb = arango_client.db(db_name)

ortholog_node_coll_name = 'ortholog_nodes'
ortholog_edge_coll_name = 'ortholog_edges'
equiv_node_coll_name = 'equivalence_nodes'
equiv_edge_coll_name = 'equivalence_edges'
