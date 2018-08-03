import falcon
import structlog
import json
import ast
import traceback

log = structlog.getLogger(__name__)


# Add API exception handler
def internal_error_handler(ex, req, resp, params):
    if not isinstance(ex, (falcon.HTTPError, falcon.HTTPStatus)):  # Check if it's a manually raised falcon.HTTPError/HTTPStatusXXX
        description = json.dumps(ast.literal_eval(str(ex)))
#        log.error(f'Dir: {dir(ex)} Ex: {ex}  Args: {ex.args}  Traceback {ex.__traceback__}')
        log.exception(ex)
        raise falcon.HTTPInternalServerError(description=f'Ex: {description}')  # HTTPError is just our own wrapper around falcon.HTTPError
    else:
        raise


def register_defaults(api):
    api.add_error_handler(Exception, internal_error_handler)
