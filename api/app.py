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

from resources.status import SimpleStatusResource, StatusResource, VersionResource

from resources.terms import TermResource
from resources.terms import TermsResource
from resources.terms import TermCompletionsResource
from resources.terms import TermEquivalentsResource
from resources.terms import TermCanonicalizeResource
from resources.terms import TermDecanonicalizeResource
from resources.terms import TermTypesResource

from resources.orthology import OrthologResource

# Setup logging
module_fn = os.path.basename(__file__)
module_fn = module_fn.replace('.py', '')

logging_conf_fn = './conf-logging.yml'
with open(logging_conf_fn, mode='r') as f:
    logging.config.dictConfig(yaml.load(f))
    log = logging.getLogger(f'{module_fn}')

cors = CORS(allow_all_origins=True)

# Allow requiring authentication via JWT
if config.authenticated:
    def user_loader(payload):
        # log.info(payload)
        return True

    auth_backend = JWTAuthBackend(
        user_loader=user_loader,
        secret_key=config.secrets.shared_secret,
        required_claims=['exp', 'iat'],
    )
    auth_middleware = FalconAuthMiddleware(
        auth_backend,
        exempt_routes=['/simple_status', '/version'],
        exempt_methods=['HEAD']
    )

    api = application = falcon.API(middleware=[auth_middleware, cors.middleware, ])

else:
    api = application = falcon.API(middleware=[cors.middleware, ])


# Routes  ###############
# Add routes to skip authentication in common/middleware:AuthMiddleware.skip_routes list

# Term routes
api.add_route('/terms', TermsResource())  # GET
api.add_route('/terms/completions/{complete_term}', TermCompletionsResource())

api.add_route('/terms/{term_id}', TermResource())  # GET
api.add_route('/terms/{term_id}/equivalents', TermEquivalentsResource())  # GET
api.add_route('/terms/{term_id}/canonicalized', TermCanonicalizeResource())  # GET
api.add_route('/terms/{term_id}/decanonicalized', TermDecanonicalizeResource())  # GET
api.add_route('/terms/types', TermTypesResource())  # GET

# Orthology routes
api.add_route('/orthologs', OrthologResource())  # GET
api.add_route('/orthologs/{gene_id}', OrthologResource())  # GET
api.add_route('/orthologs/{gene_id}/{species}', OrthologResource())  # GET

# Status endpoints - used to check that API is running correctly
api.add_route('/simple_status', SimpleStatusResource())  # un-authenticated
api.add_route('/status', StatusResource())  # authenticated
api.add_route('/version', VersionResource())  # version

# Useful for debugging problems in your API; works with pdb.set_trace()
if __name__ == '__main__':
    from wsgiref import simple_server

    host = "127.0.0.1"
    port = 8000
    httpd = simple_server.make_server(host, port, api)
    print("Serving on {}:{}".format(host, port))
    httpd.serve_forever()
