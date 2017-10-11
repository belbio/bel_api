#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import falcon
from falcon_cors import CORS
from falcon_auth import FalconAuthMiddleware, JWTAuthBackend
import logging
import logging.config
import yaml
import os

from Config import config  # Application settings enabled for Dev/Test/Prod

from resources.status import SimpleStatusResource, StatusResource
from resources.terms import TermResource, TermsResource

# Setup logging
module_fn = os.path.basename(__file__)
module_fn = module_fn.replace('.py', '')

logging_conf_fn = './conf-logging.yml'
with open(logging_conf_fn, mode='r') as f:
    logging.config.dictConfig(yaml.load(f))
    log = logging.getLogger(f'{module_fn}')

cors = CORS(allow_all_origins=True)

if config.authenticated:
    def user_loader(payload):
        # log.info(payload)
        return True

    log.info(config.secrets.shared_secret)

    auth_backend = JWTAuthBackend(
        user_loader=user_loader,
        secret_key=config.secrets.shared_secret,
        required_claims=['exp', 'iat'],
    )
    auth_middleware = FalconAuthMiddleware(
        auth_backend,
        exempt_routes=['/simple_status'],
        exempt_methods=['HEAD']
    )

    api = application = falcon.API(middleware=[auth_middleware, cors.middleware, ])

else:
    api = application = falcon.API(middleware=[cors.middleware, ])

# Routes  ###############
# Add routes to skip authentication in common/middleware:AuthMiddleware.skip_routes list

# Term routes
api.add_route('/terms', TermsResource())  # GET, POST
api.add_route('/terms/{term_id}', TermResource())  # GET, PUT, DELETE

# Status endpoints - used to check that API is running correctly
api.add_route('/simple_status', SimpleStatusResource())  # un-authenticated
api.add_route('/status', StatusResource())  # authenticated

# Useful for debugging problems in your API; works with pdb.set_trace()
if __name__ == '__main__':
    from wsgiref import simple_server

    host = "127.0.0.1"
    port = 8000
    httpd = simple_server.make_server(host, port, api)
    print("Serving on {}:{}".format(host, port))
    httpd.serve_forever()
