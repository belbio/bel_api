#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:  program.py <customer>

"""

from elasticsearch import Elasticsearch
import yaml
import logging
import logging.config

# Globals
es_conn = 'http://localhost:9200'
es = Elasticsearch([es_conn], send_get_body_as='POST')

mapping_term_fn = './es_mapping_term.yaml'
with open(mapping_term_fn, 'r') as f:
    mapping_term = yaml.load(f)


def index_exists(index):
    """
    Input: index -- index to check for existence

    """
    return es.indices.exists(index=index)


def create_terms_index():
    if index_exists('terms'):
        r = es.indices.delete(index="terms")
        log.debug('R: ', r)
    r = es.indices.create(index="terms", body=mapping_term)
    log.debug('Index create result: ', r)


def main():
    create_terms_index()


if __name__ == '__main__':
    # Setup logging
    global log

    logging_conf_fn = '../logging-conf.yaml'
    with open(logging_conf_fn, mode='r') as f:
        logging.config.dictConfig(yaml.load(f))
        log = logging.getLogger(__name__)

    main()

