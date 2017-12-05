#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:  program.py <customer>

"""

from arango import ArangoClient, ArangoError
from typing import Mapping, Dict, List, Any, Optional, Union, Tuple
import logging
import re

from bel_lang.Config import config

log = logging.getLogger(__name__)

arango_client = ArangoClient(
    protocol=config['bel_api']['servers']['arangodb_protocol'],
    host=config['bel_api']['servers']['arangodb_host'],
    port=config['bel_api']['servers']['arangodb_port'],
    username=config['bel_api']['servers']['arangodb_username'],
    password=config['secrets']['bel_api']['servers']['arangodb_password'],
    enable_logging=True,
)

db_name = 'bel'
arangodb = arango_client.db(db_name)

ortholog_node_coll_name = 'ortholog_nodes'
ortholog_edge_coll_name = 'ortholog_edges'
equiv_node_coll_name = 'equivalence_nodes'
equiv_edge_coll_name = 'equivalence_edges'


def arango_id_to_key(_id):
    """Remove illegal chars from potential arangodb _key (id)

    Args:
        _id (str): id to be used as arangodb _key

    Returns:
        (str): _key value with illegal chars removed
    """

    key = re.sub("[^a-zA-Z0-9\_\-\:\.\@\(\)\+\,\=\;\$\!\*\'\%]+", '_', _id)
    if len(key) > 254:
        log.error(f'Arango _key cannot be longer than 254 chars: Len={len(key)}  Key: {key}')
    return key

