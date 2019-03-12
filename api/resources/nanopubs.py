import falcon
import services.edges
import json
import fastcache
import traceback

import bel.nanopub.validate

import structlog

log = structlog.getLogger(__name__)


class NanopubValidateResource(object):
    """Validate nanopubs"""

    def on_post(self, req, resp):

        # BEL Resources loading
        try:
            data = json.load(req.bounded_stream)
        except ValueError as e:
            raise falcon.HTTPUnprocessableEntity(
                title="Cannot process payload",
                description=f"Cannot process nanopub (maybe an encoding error? please use UTF-8 for JSON payload) error: {str(e)}",
            )

        if data.get("nanopub", None) is not None:
            response_type = data.get("response_type", "nanopub")
            error_level = data.get("error_level", "WARNING")
            nanopub = {"nanopub": data.get("nanopub")}
            try:
                results = bel.nanopub.validate.validate(nanopub, error_level)
                log.info(f"Validation results: {results}")
                if response_type == "nanopub":
                    nanopub["nanopub"]["metadata"]["gd_validation"] = results
                    resp.media = nanopub
                else:
                    resp.media = {"validation_results": results}
                resp.status = falcon.HTTP_200
            except Exception as e:
                log.error(traceback.print_exc())
                raise falcon.HTTPUnprocessableEntity(
                    title="Cannot process nanopub", description=f"Cannot process nanopub: {str(e)}"
                )

        else:
            raise falcon.HTTPBadRequest(
                title="Cannot process nanopub",
                description=f"No nanopub in payload to process. Please check your submission.",
            )


class EdgeResource(object):
    """Edge endpoint"""

    @fastcache.clru_cache(maxsize=500)
    def on_get(self, req, resp, edge_id=None):
        """GET Edge using edge_id

        This will return the record if it finds the edge_id in the EdgeStore.
        """

        if edge_id is None:
            resp.media = {
                "title": "EdgeStore endpoint Error",
                "message": "Must provide an edge id, e.g. /edges/139806548404171878991929958738371273692",
            }
            resp.status = falcon.HTTP_200
            return

        edge = services.edges.get_edge(edge_id)
        if edge:
            resp.media = edge
            resp.status = falcon.HTTP_200
        else:
            description = "No edge found for {}".format(edge_id)
            resp.media = {"title": "No Edge", "message": description}
            resp.status = falcon.HTTP_404


class EdgesResource(object):
    """Edges endpoint"""

    def on_get(self, req, resp):
        """GET Edges from EdgeStore"""

        # Query parameters
        node_query = req.get_param("node_query", default="")
        hops = req.get_param("hops", default=1)
        direction = req.get_param("direction", default="ANY")
        if direction not in ["ANY", "INBOUND", "OUTBOUND"]:
            message = "Query parameter: direction must be one of ('ANY', 'INBOUND', 'OUTBOUND')"
            title = "Bad query parameter"
            raise falcon.HTTPBadRequest(title=title, description=message)

        contains = req.get_param_as_bool("contains") or False
        filters = req.get_param("filters", default=None)
        limit = req.get_param_as_int("limit", min=1, max=1000) or 1000
        offset = req.get_param_as_int("offset", min=0) or 0

        (edges, facets) = services.edges.get_edges(
            node_query,
            hops=hops,
            direction=direction,
            contains=contains,
            filters=filters,
            limit=limit,
            offset=offset,
        )

        resp.media = {"edges": edges, "facets": facets, "edge_cnt": len(edges)}
        resp.status = falcon.HTTP_200
