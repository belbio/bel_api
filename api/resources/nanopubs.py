import json
import traceback
import unicodedata

import bel.nanopub.validate
import falcon
import fastcache
import structlog

log = structlog.getLogger(__name__)


class NanopubValidateResource(object):
    """Validate nanopubs"""

    def on_post(self, req, resp):

        # BEL Resources loading
        try:
            data = req.stream.read(req.content_length or 0)
            data = data.decode(encoding="utf-8")
            data = data.replace("\u00a0", " ")  # get rid of non-breaking spaces
            data = json.loads(data)
        except ValueError as e:
            raise falcon.HTTPUnprocessableEntity(
                title="Cannot process payload",
                description=f"Cannot process nanopub (maybe an encoding error? please use UTF-8 for JSON payload) error: {e}",
            )

        nanopub = {}
        if "nanopub" in data:
            nanopub["nanopub"] = data.get("nanopub")
        else:
            nanopub = None
        error_level = data.get("error_level", "WARNING")

        if nanopub:
            try:
                results = bel.nanopub.validate.validate(nanopub, error_level)
                nanopub["nanopub"]["metadata"]["gd_validation"] = results
                log.debug(f"Validation Results: {results}")
                resp.media = nanopub
                resp.status = falcon.HTTP_200
            except Exception as e:
                log.error(traceback.print_exc())
                raise falcon.HTTPUnprocessableEntity(
                    title="Cannot process nanopub", description=f"Cannot process nanopub: {e}"
                )

        else:
            raise falcon.HTTPBadRequest(
                title="Cannot process nanopub",
                description=f"No nanopub in payload to process. Please check your submission.",
            )
