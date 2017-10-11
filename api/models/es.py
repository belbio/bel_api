#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Config import config
from elasticsearch import Elasticsearch
import logging

log = logging.getLogger(__name__)

es = Elasticsearch([config.servers.elasticsearch], send_get_body_as='POST')


def index_exists(index):
    """
    Input: index -- index to check for existence

    """
    return es.indices.exists(index=index)


def namespace_term_counts():
    """Generate counts of each namespace in terms index

    This function is at least used in the /status endpoint to show how many
    terms are in each namespace and what namespaces are available.

    Returns:
        List[Mapping[str, int]]: array of namespace vs counts
    """

    search_body = {
        "aggs": {
            "namespace_term_counts": {"terms": {"field": "namespace"}}
        }
    }

    results = es.search(index='terms', doc_type='term', body=search_body, size=0)
    results = results['aggregations']['namespace_term_counts']['buckets']

    # return results
    return [{'namespace': r['key'], 'count': r['doc_count']} for r in results]


def main():
    pass


if __name__ == '__main__':
    main()
