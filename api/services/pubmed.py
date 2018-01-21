from typing import MutableMapping, Mapping, Any
import copy

import bel.nanopub.pubmed
import services.terms as terms
# from bel.Config import config

# import timy
# from timy.settings import (
#     timy_config,
#     TrackingMode
# )
# timy_config.tracking_mode = TrackingMode.LOGGING

import logging
log = logging.getLogger(__name__)


def enhance_pubmed_annotations(pubmed: MutableMapping[str, Any]) -> Mapping[str, Any]:
    """Enhance Pubmed object

    Add additional entity and annotation types to annotations
    Use preferred id for namespaces as needed
    Add strings from Title, Abstract matching Pubtator BioConcept spans

    NOTE - basically duplicated code with bel:bel.nanopub.pubmed - just uses
            internal function calls instead of bel_api calls

    Args:
        pubmed

    Returns:
        pubmed object
    """

    text = pubmed['title'] + pubmed['abstract']

    annotations = {}

    for nsarg in pubmed['annotations']:
        term = terms.get_term(nsarg)

        if term:
            new_nsarg = terms.decanonicalize(term['id'])
            pubmed['annotations'][nsarg]['name'] = term['name']
            pubmed['annotations'][nsarg]['label'] = term['label']
            pubmed['annotations'][nsarg]['entity_types'] = list(set(pubmed['annotations'][nsarg]['entity_types'] + term.get('entity_types', [])))
            pubmed['annotations'][nsarg]['annotation_types'] = list(set(pubmed['annotations'][nsarg]['annotation_types'] + term.get('annotation_types', [])))

            if new_nsarg != nsarg:
                annotations[new_nsarg] = copy.deepcopy(pubmed['annotations'][nsarg])
            else:
                annotations[nsarg] = copy.deepcopy(pubmed['annotations'][nsarg])

    for nsarg in annotations:
        for idx, span in enumerate(annotations[nsarg]['spans']):
            string = text[span['begin'] - 1:span['end'] - 1]
            annotations[nsarg]['spans'][idx]['text'] = string

    pubmed['annotations'] = copy.deepcopy(annotations)

    return pubmed


def get_pubmed_for_beleditor(pmid: str, pubmed_only_flag: bool) -> Mapping[str, Any]:
    """Get Pubmed info used by BEL Editor

    This enhances the Pubmed return object with BEL.bio API preferred
    namespaces and Pubtator Bioconcept results (annotations subobject).

    Args:
        pmid: Pubmed ID
        pubmed_only_flag: only get Pubmed info, not Pubtator annotations

    Returns:
        Mapping[str, Any]: json object with Pubmed info
    """
    #with timy.Timer() as timer:
    pubmed = bel.nanopub.pubmed.get_pubmed(pmid)
    # timer.track('Got pubmed')
    # Get Bioconcepts extracted from Title, Abstract
    if not pubmed_only_flag:
        pubtator = bel.nanopub.pubmed.get_pubtator(pmid)
        # timer.track('Got pubtator')

        if pubtator:
            pubmed['annotations'] = copy.deepcopy(pubtator['annotations'])
            # timer.track('Enhanced pubmed')

            # Add entity types and annotation types to annotations
            pubmed = enhance_pubmed_annotations(pubmed)

    return pubmed

