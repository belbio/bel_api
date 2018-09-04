#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gevent.monkey
gevent.monkey.patch_all()

import os

import falcon
from falcon_cors import CORS
from falcon_auth import FalconAuthMiddleware, JWTAuthBackend

# import logging
# import logging.config
# # from pythonjsonlogger import jsonlogger
import bel.setup_logging
import bel.lang.bel_specification  # updates BEL Specification every time API starts

from bel.Config import config

import services.swaggerui

from middleware.stats import FalconStatsMiddleware
import middleware.falcon_exceptions

import routes

# TODO - figure out how to run logging setup and belspec once on startup rather than
#        every time a worker is initialized (moved bel.lang.bel_specification.update_specifications to bel/__init__.py)

import bel.setup_logging
import structlog
log = structlog.getLogger('bel_api')

cors = CORS(allow_all_origins=True, allow_all_methods=True, allow_all_headers=True, allow_credentials_all_origins=True)

stats_middleware = FalconStatsMiddleware()

# Allow requiring authentication via JWT
if config['bel_api']['authenticated']:

    # Loads user data from JWT
    def user_loader(payload):
        # log.info(payload)
        return True

    auth_backend = JWTAuthBackend(
        user_loader=user_loader,
        secret_key=config['secrets']['bel_api']['shared_secret'],
        required_claims=['exp', 'iat'],
    )
    auth_middleware = FalconAuthMiddleware(
        auth_backend,
        exempt_routes=['/simple_status', '/healthcheck', '/version', ],
        exempt_methods=['HEAD']
    )

    api = application = falcon.API(middleware=[stats_middleware, auth_middleware, cors.middleware, ])

else:
    api = application = falcon.API(middleware=[stats_middleware, cors.middleware, ])

# Add exception handling
middleware.falcon_exceptions.register_defaults(api)

# Add Swagger UI
services.swaggerui.register_swaggerui(api)

# Routes  ###############
# Add routes to skip authentication in common/middleware:AuthMiddleware.skip_routes list
routes.add_routes(api)


# Useful for debugging problems in your API; works with pdb.set_trace()
if __name__ == '__main__':
    from wsgiref import simple_server

    host = "127.0.0.1"
    port = 8181
    httpd = simple_server.make_server(host, port, api)
    print("Serving on {}:{}".format(host, port))
    httpd.serve_forever()
