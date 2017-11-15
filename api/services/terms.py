import elasticsearch
import falcon
from typing import Mapping, Dict, List, Any, Optional, Union, Tuple
import re

from models.es import es
from models.arangodb import arangodb

import Config
from Config import config

import logging
log = logging.getLogger(__name__)


def get_species_info(species_id):

    log.info(species_id)

    url_template = "https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Info&lvl=3&lin=f&keep=1&srchmode=1&unlock&id=<src_id>"
    search_body = {
        "_source": ["src_id", "id", "name", "label", "taxonomy_rank"],
        "query": {
            "term": {"id": species_id}
        }
    }

    result = es.search(index='terms', doc_type='term', body=search_body)
    src = result['hits']['hits'][0]['_source']
    url = re.sub('(<src_id>)', src['src_id'], url_template)
    src['url'] = url
    del src['src_id']
    return src


def get_species_object(species_id):

    species = get_species_info(species_id)
    return {"id": species['id'], "label": species['label']}


def get_term(term_id):
    """Get term using term_id

    Term ID has to match either the id or the alt_ids
    """
    search_body = {
        "query": {
            "bool": {
                "should": [
                    {"term": {"id": term_id}},
                    {"term": {"alt_ids": term_id}},
                ]
            }
        }
    }

    result = es.search(index='terms', doc_type='term', body=search_body)
    # import json
    # print('DumpVar:\n', json.dumps(result, indent=4))
    if len(result['hits']['hits']) > 0:
        result = result['hits']['hits'][0]['_source']
        del result['completions']
    else:
        result = None

    return result


def get_term_completions(complete_term, size, context_filter):
    """Get Term completions filtered by context

    """
    search_body = {
        "_source": ["id", "name", "label", "description", "species_id", "species_label"],
        "suggest": {
            "term-suggest": {
                "prefix": complete_term,
                "completion": {
                    "field": "completions",
                    "size": size,
                }
            }
        }
    }

    if context_filter:
        search_body['suggest']['term-suggest']['completion']['contexts'] = context_filter

    results = es.search(index='terms', doc_type='term', body=search_body)

    # highlight matches
    completions = []
    for option in results['suggest']['term-suggest'][0]['options']:
        match = re.sub(f'({complete_term})', r"<em>\1<em>", option['text'], flags=re.IGNORECASE)

        species_id = option['_source'].get('species_id', None)
        species_label = option['_source'].get('species_label', None)
        species = {'id': species_id, 'label': species_label}
        completions.append({
            "id": option['_source']["id"],
            "name": option['_source']['name'],
            "label": option['_source']['label'],
            "description": option['_source'].get('description', None),
            "species": species,
            "match": match,
        })

    return completions


def term_types():
    """Collect Term Types and their counts

    Return aggregations of namespaces, entity types, and context types
    up to a 100 of each type (see size=<number> in query below)

    Returns:
        Mapping[str, Mapping[str, int]]: dict of dicts for term types
    """

    size = 100

    search_body = {
        "aggs": {
            "namespace_term_counts": {"terms": {"field": "namespace", "size": size}},
            "entity_type_counts": {"terms": {"field": "entity_types", "size": size}},
            "context_type_counts": {"terms": {"field": "context_types", "size": size}},
        }
    }

    results = es.search(index='terms', doc_type='term', body=search_body, size=0)

    types = {'namespaces': {}, 'entity_types': {}, 'context_types': {}}

    aggs = {
        "namespace_term_counts": "namespaces",
        "entity_type_counts": "entity_types",
        "context_type_counts": "context_types",
    }
    for agg in aggs:
        for bucket in results['aggregations'][agg]['buckets']:
            types[aggs[agg]][bucket['key']] = bucket['doc_count']

    return types


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

    # Get term counts but raise error if elasticsearch is not available
    try:
        results = es.search(index='terms', doc_type='term', body=search_body, size=0)
        results = results['aggregations']['namespace_term_counts']['buckets']
    except elasticsearch.ConnectionError as e:
        raise falcon.HTTPBadRequest(
            title='Connection Refused',
            description='Cannot access Elasticsearch',
        )

    # return results
    return [{'namespace': r['key'], 'count': r['doc_count']} for r in results]


def get_equivalents(term_id: str, namespaces: List[str]=None) -> List[Mapping[str, str]]:
    """Get equivalents given ns:id and target namespaces

    The target_namespaces list in the argument dictionary is ordered by priority.

    Args:
        term_id (str): term id
        namespaces (Mapping[str, Any]): filter resulting equivalents to listed namespaces, ordered by priority

    Returns:
        List[Mapping[str, str]]: e.g. [{'term_id': 'HGNC:5', 'namespace': 'EG'}]
    """

    query = f"FOR vertex, edge IN 1..10 ANY 'equivalence_nodes/{term_id}' equivalence_edges " + "RETURN {term_id: vertex._key, namespace: vertex.namespace}"
    cursor = arangodb.aql.execute(query)

    equivalents = {}
    for record in cursor:
        equivalents[record['namespace']] = record['term_id']

    return equivalents


def canonicalize(term_id: str, namespace_targets: Mapping[str, List[str]] = None) -> str:
    """Canonicalize term_id

    Convert term namespace to canonical namespaces pulling them from
    the settings ArangoDB collection (e.g. the API configured canonical
    namespace mappings) if not given. The target namespaces are ordered
    and the first namespace:id found will be returned.

    For example, given HGNC:A1BG, this function will return EG:1 if
    namespace_targets={'HGNC': [EG', 'SP']}

    Args:
        term_id (str): term to canonicalize
        namespace_targets (Mapping[str, List[str]]): Map of namespace targets to convert term into

    Returns:
        str: return canonicalized term if available, else the original term_id
    """

    if not namespace_targets:
        namespace_targets = Config.get_canonical_settings()['canonical']

    for start_ns in namespace_targets:
        if re.match(start_ns, term_id):
            equivalents = get_equivalents(term_id)
            # log.info(f'Equiv: {equivalents}')
            for target_ns in namespace_targets[start_ns]:
                if target_ns in equivalents:
                    term_id = equivalents[target_ns]

    return term_id


def decanonicalize(term_id: str, namespace_targets: Mapping[str, List[str]] = None) -> str:
    """De-canonicalize term_id

    Convert term namespace to user friendly namespaces pulling them from
    the settings ArangoDB collection (e.g. the API configured decanonical
    namespace mappings) if not given. The target namespaces are ordered
    and the first namespace:id found will be returned.

    For example, given EG:1, this function will return HGNC:A1BG if
    namespace_targets={'EG': [HGNC', 'MGI', 'RGD', 'SP'], 'SP': [HGNC', 'MGI', 'RGD']}

    Args:
        term_id (str): term to decanonicalize
        namespace_targets (Mapping[str, List[str]]): Map of namespace targets to convert term into

    Returns:
        str: return decanonicalized term if available, else the original term_id
    """

    if not namespace_targets:
        namespace_targets = Config.get_canonical_settings()['decanonical']

    for start_ns in namespace_targets:
        if re.match(start_ns, term_id):
            equivalents = get_equivalents(term_id)
            log.info(f'Equiv: {equivalents}')
            for target_ns in namespace_targets[start_ns]:
                if target_ns in equivalents:
                    term_id = equivalents[target_ns]

    return term_id
