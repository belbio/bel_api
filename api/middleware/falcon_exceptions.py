import falcon
import structlog

log = structlog.getLogger(__name__)


# Add API exception handler
def internal_error_handler(ex, req, resp, params):
    if not isinstance(ex, (falcon.HTTPError, falcon.HTTPStatus)):  # Check if it's a manually raised falcon.HTTPError/HTTPStatusXXX
        log.error(ex)
        raise falcon.HTTPInternalServerError(description=f'Ex: {repr(ex)}')  # HTTPError is just our own wrapper around falcon.HTTPError
    else:
        raise


def register_defaults(api):
    api.add_error_handler(Exception, internal_error_handler)
