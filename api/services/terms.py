import elasticsearch
import falcon
from typing import Mapping, List, Union
import re

import bel.db.elasticsearch
import bel.db.arangodb

from bel.Config import config

# import logging
# log = logging.getLogger(__name__)

import structlog

log = structlog.getLogger()

es = bel.db.elasticsearch.get_client()

arangodb_client = bel.db.arangodb.get_client()
belns_db = bel.db.arangodb.get_belns_handle(arangodb_client)


def get_species_info(species_id):

    log.debug(species_id)

    url_template = "https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Info&lvl=3&lin=f&keep=1&srchmode=1&unlock&id=<src_id>"
    search_body = {
        "_source": ["src_id", "id", "name", "label", "taxonomy_rank"],
        "query": {"term": {"id": species_id}},
    }

    result = es.search(index="terms", doc_type="term", body=search_body)
    src = result["hits"]["hits"][0]["_source"]
    url = re.sub("(<src_id>)", src["src_id"], url_template)
    src["url"] = url
    del src["src_id"]
    return src


def get_species_object(species_id):

    species = get_species_info(species_id)
    return {"id": species["id"], "label": species["label"]}


# TODO Refactor to use bel.terms.terms.get_terms
def get_term(term_id):
    """Get first matching term using term_id

    Term ID has to match either the id or the alt_ids
    """
    search_body = {
        "query": {
            "bool": {
                "should": [
                    {"term": {"id": term_id}},
                    {"term": {"alt_ids": term_id}},
                    {"term": {"obsolete_ids": term_id}},
                ]
            }
        }
    }

    result = es.search(index="terms", doc_type="term", body=search_body)

    if len(result["hits"]["hits"]) > 0:
        result = result["hits"]["hits"][0]["_source"]
    else:
        result = None

    return result


# TODO Refactor to use bel.terms.terms.get_terms
def get_terms(term_id):
    """Get term(s) using term_id - given term_id may match multiple term records

    Term ID has to match either the id, alt_ids or obsolete_ids
    """
    search_body = {
        "query": {
            "bool": {
                "should": [
                    {"term": {"id": term_id}},
                    {"term": {"alt_ids": term_id}},
                    {"term": {"obsolete_ids": term_id}},
                ]
            }
        }
    }

    result = es.search(index="terms", doc_type="term", body=search_body)

    results = []
    for r in result["hits"]["hits"]:
        results.append(r["_source"])

    return results


# TODO - not deployed/fully implemented
def get_term_search(search_term, size, entity_types, annotation_types, species, namespaces):
    """Search for terms given search term

        to be used for /terms POST endpoint
    """

    if not size:
        size = 10

    filters = []
    if entity_types:
        filters.append({"terms": {"entity_types": entity_types}})
    if annotation_types:
        filters.append({"terms": {"annotation_types": annotation_types}})
    if species:
        filters.append({"terms": {"species": species}})
    if namespaces:
        filters.append({"terms": {"namespaces": namespaces}})

    search_body = {
        "size": size,
        "query": {
            "bool": {
                "minimum_should_match": 1,
                "should": [
                    {"match": {"id": {"query": "", "boost": 4}}},
                    {"match": {"namespace_value": {"query": "", "boost": 4}}},
                    {"match": {"name": {"query": "", "boost": 2}}},
                    {"match": {"synonyms": {"query": ""}}},
                    {"match": {"label": {"query": "", "boost": 4}}},
                    {"match": {"alt_ids": {"query": "", "boost": 2}}},
                    {"match": {"src_id": {"query": ""}}},
                ],
                "filter": filters,
            }
        },
        "highlight": {
            "fields": [
                {"id": {}},
                {"name": {}},
                {"label": {}},
                {"synonyms": {}},
                {"alt_ids": {}},
                {"src_id": {}},
            ]
        },
    }

    results = es.search(index="terms", doc_type="term", body=search_body)

    search_results = []
    for result in results["hits"]["hits"]:
        search_results.append(result["_source"] + {"highlight": result["highlight"]})

    return search_results


def get_term_completions(
    completion_text, size, entity_types, annotation_types, species, namespaces
):
    """Get Term completions filtered by additional requirements

    Args:
        completion_text: text to complete to location NSArgs
        size: how many terms to return
        entity_types: list of entity_types used to filter completion results
        annotation_types: list of annotation types used to filter completion results
        species: list of species (TAX:nnnn) used to filter completions
        namespaces: list of namespaces to filter completions

    Returns:
        list of NSArgs
    """
    log.info(f"Size: {size}")
    # Split out Namespace from namespace value to use namespace for filter
    #     and value for completion text
    matches = re.match('([A-Z]+):"?(.*)', completion_text)
    if matches:
        namespaces = [matches.group(1)]
        completion_text = matches.group(2)

    if species == [None]:
        species = []

    if namespaces == [None]:
        namespaces = []

    if annotation_types == [None]:
        annotation_types = []

    if entity_types == [None]:
        entity_types = []

    filters = []

    # Entity filters
    if entity_types and isinstance(entity_types, str):
        entity_types = [entity_types]
        filters.append({"terms": {"entity_types": entity_types}})
    elif entity_types:
        filters.append({"terms": {"entity_types": entity_types}})

    # Annotation type filters
    if annotation_types and isinstance(annotation_types, str):
        filters.append({"terms": {"annotation_types": [annotation_types]}})
    elif annotation_types:
        filters.append({"terms": {"annotation_types": annotation_types}})

    # Namespace filter
    if namespaces and isinstance(namespaces, str):
        filters.append({"terms": {"namespace": [namespaces]}})
    elif namespaces:
        filters.append({"terms": {"namespace": namespaces}})

    # Species filter
    grp = False
    if entity_types:
        grp = [
            et for et in entity_types if et in config["bel_api"]["search"]["species_entity_types"]
        ]

    if grp and species:
        if isinstance(species, str):
            species = [species]

        # Allow non-species specific terms to be found
        filters.append(
            {
                "bool": {
                    "should": [
                        {"bool": {"must_not": {"exists": {"field": "species_id"}}}},
                        {"terms": {"species_id": species}},
                    ]
                }
            }
        )

    log.info(f"Term Filters {filters}")

    search_body = {
        "_source": [
            "id",
            "name",
            "label",
            "description",
            "species_id",
            "species_label",
            "entity_types",
            "annotation_types",
            "synonyms",
        ],
        "size": size,
        "query": {
            "bool": {
                "should": [
                    {"match": {"id": {"query": completion_text, "boost": 6, "_name": "id"}}},
                    {
                        "match": {
                            "namespace_value": {
                                "query": completion_text,
                                "boost": 8,
                                "_name": "namespace_value",
                            }
                        }
                    },
                    {"match": {"label": {"query": completion_text, "boost": 5, "_name": "label"}}},
                    {
                        "match": {
                            "synonyms": {"query": completion_text, "boost": 1, "_name": "synonyms"}
                        }
                    },
                ],
                "must": {
                    "match": {"autocomplete": {"query": completion_text, "_name": "autocomplete"}}
                },
                "filter": filters,
            }
        },
        "highlight": {"fields": {"autocomplete": {"type": "plain"}, "synonyms": {"type": "plain"}}},
    }

    import json

    log.debug(f"Completion search body {json.dumps(search_body)}")

    # Boost namespaces
    if config["bel_api"].get("search", False):
        if config["bel_api"]["search"].get("boost_namespaces", False):
            if not isinstance(config["bel_api"]["search"]["boost_namespaces"], (list)):
                log.warn("BEL config boost_namespaces is not an array (list)!")
            else:
                boost_namespaces = {
                    "terms": {
                        "namespace": config["bel_api"]["search"]["boost_namespaces"],
                        "boost": 6,
                    }
                }
                search_body["query"]["bool"]["should"].append(boost_namespaces)

    results = es.search(index="terms", doc_type="term", body=search_body)

    # highlight matches
    completions = []

    for result in results["hits"]["hits"]:
        species_id = result["_source"].get("species_id", None)
        species_label = result["_source"].get("species_label", None)
        species = {"id": species_id, "label": species_label}
        entity_types = result["_source"].get("entity_types", None)
        annotation_types = result["_source"].get("annotation_types", None)
        # Filter out duplicate matches
        matches = []
        matches_lower = []
        for match in result["highlight"]["autocomplete"]:
            if match.lower() in matches_lower:
                continue
            matches.append(match)
            matches_lower.append(match.lower())

        completions.append(
            {
                "id": result["_source"]["id"],
                "name": result["_source"].get("name", "Missing Name"),
                "label": result["_source"].get("label", "Missing Label"),
                "description": result["_source"].get("description", None),
                "species": species,
                "entity_types": entity_types,
                "annotation_types": annotation_types,
                "highlight": matches,
            }
        )

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
            "annotation_type_counts": {"terms": {"field": "annotation_types", "size": size}},
        }
    }

    results = es.search(index="terms", doc_type="term", body=search_body, size=0)

    types = {"namespaces": {}, "entity_types": {}, "annotation_types": {}}

    aggs = {
        "namespace_term_counts": "namespaces",
        "entity_type_counts": "entity_types",
        "annotation_type_counts": "annotation_types",
    }
    for agg in aggs:
        for bucket in results["aggregations"][agg]["buckets"]:
            types[aggs[agg]][bucket["key"]] = bucket["doc_count"]

    return types


def namespace_term_counts():
    """Generate counts of each namespace in terms index

    This function is at least used in the /status endpoint to show how many
    terms are in each namespace and what namespaces are available.

    Returns:
        List[Mapping[str, int]]: array of namespace vs counts
    """

    size = 100

    search_body = {
        "aggs": {"namespace_term_counts": {"terms": {"field": "namespace", "size": size}}}
    }

    # Get term counts but raise error if elasticsearch is not available
    try:
        results = es.search(index="terms", doc_type="term", body=search_body, size=0)
        results = results["aggregations"]["namespace_term_counts"]["buckets"]
    except elasticsearch.ConnectionError as e:
        raise falcon.HTTPBadRequest(
            title="Connection Refused", description="Cannot access Elasticsearch"
        )

    # return results
    return [{"namespace": r["key"], "count": r["doc_count"]} for r in results]


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
        namespace_targets = config["bel"]["lang"]["canonical"]

    for start_ns in namespace_targets:
        if re.match(start_ns, term_id):
            results = bel.terms.terms.get_equivalents(term_id)
            equivalents = results["equivalents"]
            for target_ns in namespace_targets[start_ns]:
                for e in equivalents:
                    if target_ns in e["namespace"] and e["primary"]:
                        return e["term_id"]

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
        namespace_targets = config["bel"]["lang"]["decanonical"]

    for start_ns in namespace_targets:
        if re.match(start_ns, term_id):
            results = bel.terms.terms.get_equivalents(term_id)
            equivalents = results["equivalents"]
            log.debug(f"Term: {term_id} Equiv: {equivalents}")
            for target_ns in namespace_targets[start_ns]:
                for e in equivalents:
                    if target_ns in e["namespace"] and e["primary"]:
                        return e["term_id"]

    return term_id
