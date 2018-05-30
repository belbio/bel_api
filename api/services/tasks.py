from time import sleep
import datetime
from typing import List

import bel.utils
import bel.edge.edges
import bel.resources.resource
import bel.nanopub.nanopubstore as nanopubstore
from common.celery import celery_app

import structlog
log = structlog.getLogger(__name__)


def queue_nanopubs(nanopubstore_url: str, start_dt: str, orthologize_targets: List[str] = []):
    """Add new Public nanopubs to task queue to convert to edges

    Add all Public Nanopubs from nanopubstore_url more recent than
    start_dt to bel_pipeline queue.

    Args:
        nanopubstore_url: API url for NanopubStore (e.g. https://nanopubstore.demo.biodati.com)
        start_dt: start datetime to begin processing nanopubs
        orthology_targets: list of TAX:<ids> to convert edges into
    """

    if not start_dt:
        start_dt = nanopubstore.get_nanopubstore_start_dt(nanopubstore_url)

    # Also updates start_dt
    nanopub_urls = nanopubstore.get_new_nanopub_urls(ns_root_url=nanopubstore_url, start_dt=start_dt)
    log.info(f'Queueing Nanopubs:  start_dt {start_dt}  Num Nanopub URLS {len(nanopub_urls)}')

    for nanopub_url in nanopub_urls:
        nanopub_to_edge.delay(nanopub_url, orthologize_targets)

    return len(nanopub_urls)


@celery_app.task(ignore_result=True)
def nanopub_to_edge(nanopub_url: str, orthology_targets: List[str] = []):
    """Convert Nanopubs to Edges and load in EdgeStore

    Args:
        nanopub_url: Nanopub URL
        orthology_targets: list of species TAX:<ids>
    """

    result = bel.edge.edges.process_nanopub(nanopub_url, orthology_targets)

    return result


@celery_app.task
def add_namespace(resource_url):
    """Add BEL resource_url to bel_resources queue"""

    bel.resources.resource.load_resource(resource_url)

