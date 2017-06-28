import falcon
import logging
from Config import config
from common.authentication import jwt_validate
import json

logger = logging.getLogger('root.falcon_middleware')


class AuthMiddleware(object):

    def process_request(self, req, resp):

        if not config.authenticated:  # Skip if authentication disabled
            return

        # Don't authenticate following routes
        skip_routes = ['/simple-status']

        if req.path in skip_routes:
            logger.debug('Skipped route: {}'.format(req.path))
            return

        token = req.get_header('X-Auth-Token')

        logger.info('Path: {} Token: '.format(req.path))

        if token is None:
            description = ('Please provide an auth token '
                           'as part of the request.')

            raise falcon.HTTPUnauthorized('Auth token required',
                                          description,
                                          href='http://docs.example.com/auth')

        if not self._token_is_valid(token):
            description = ('The provided auth token is not valid. '
                           'Please request a new token and try again.')

            raise falcon.HTTPUnauthorized('Authentication required',
                                          description,
                                          href='http://docs.example.com/auth',
                                          scheme='Token; UUID')

    def _token_is_valid(self, token):
        return jwt_validate(token)[0]  # Return first result which is boolean value


class RequireJSON(object):

    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.',
                href='http://docs.examples.com/api/json')

        if req.method in ('POST', 'PUT'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.',
                    href='http://docs.examples.com/api/json')


class JSONTranslator(object):

    """Converts JSON and BSON - uses pymongo bson utils for conversion"""

    def process_request(self, req, resp):
        # req.stream corresponds to the WSGI wsgi.input environ variable,
        # and allows you to read bytes from the request body.
        #
        # See also: PEP 3333
        if req.content_length in (None, 0):
            # Nothing to do
            return

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')

        try:
            req.context['doc'] = json.loads(body.decode('utf-8'))

        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

    def process_response(self, req, resp, resource):
        if 'result' not in req.context:
            return

        resp.body = json.dumps(req.context['result'])


class RequireHTTPS(object):

    """Force the connection to be HTTPS.

    Middleware that intercepts all the requests and checks that is over an HTTPS
    protocol before continuing. The only exception to this is the DEBUG mode,
    in which we allow connections from non-HTTPS sources.

    Raises:
        HTTP Bad Request: If the connection is not HTTPS the API will complain

    Returns:
        JSON: Error mentioning the HTTPS connection is required
    """

    def process_request(self, req, resp):
        if req.protocol == "http" and not config.DEBUG:
            raise falcon.HTTPBadRequest(title="Client error. HTTP Not Allowed",
                                        description="API connections over HTTPS only.",
                                        href=config.apiDocUrl)
