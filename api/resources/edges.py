import falcon
import services.edges
import json
import fastcache

import bel.edge.edges

import structlog
log = structlog.getLogger(__name__)


class EdgesFromNanopubResource(object):
    """Edges from Nanopub"""

    def on_post(self, req, resp):
        """Build edge objects from nanopub"""

        doc = json.load(req.bounded_stream)
        if 'nanopub_url' in doc:
            result = bel.edge.edges.process_nanopub(nanopub_url=doc['nanopub_url'], orthologize_targets=doc.get('orthologize_targets', []))
        elif 'nanopub' in doc:
            result = bel.edge.edges.process_nanopub(nanopub=doc, orthologize_targets=doc.get('orthologize_targets', []))
        else:
            raise falcon.HTTPBadRequest(title='No nanopub to process', description=f"No nanopub or nanopub_url in query params to process. Please check your submission.")

        resp.media = {'edges': result}
        resp.status = falcon.HTTP_200


class EdgeResource(object):
    """Edge endpoint"""

    @fastcache.clru_cache(maxsize=500)
    def on_get(self, req, resp, edge_id=None):
        """GET Edge using edge_id

        This will return the record if it finds the edge_id in the EdgeStore.
        """

        if edge_id is None:
            resp.media = {'title': 'EdgeStore endpoint Error', 'message': 'Must provide an edge id, e.g. /edges/139806548404171878991929958738371273692'}
            resp.status = falcon.HTTP_200
            return

        edge = services.edges.get_edge(edge_id)
        if edge:
            resp.media = edge
            resp.status = falcon.HTTP_200
        else:
            description = 'No edge found for {}'.format(edge_id)
            resp.media = {'title': 'No Edge', 'message': description}
            resp.status = falcon.HTTP_404

