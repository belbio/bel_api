#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import falcon
from falcon_cors import CORS
from falcon_auth import FalconAuthMiddleware, JWTAuthBackend
import logging
import logging.config
import os

from bel.Config import config
from middleware.stats import FalconStatsMiddleware

from resources.status import SimpleStatusResource, StatusResource, VersionResource

from resources.bel_lang import BelVersions
from resources.bel_lang import BelSpecificationResource
from resources.bel_lang import BelCompletion

from resources.terms import TermResource
from resources.terms import TermsResource
from resources.terms import TermCompletionsResource
from resources.terms import TermEquivalentsResource
from resources.terms import TermCanonicalizeResource
from resources.terms import TermDecanonicalizeResource
from resources.terms import TermTypesResource

from resources.orthology import OrthologResource

from resources.pubmed import PubmedResource

# Setup logging
module_fn = os.path.basename(__file__)
module_fn = module_fn.replace('.py', '')

logging.config.dictConfig(config['logging'])
log = logging.getLogger(f'{module_fn}')

cors = CORS(allow_all_origins=True)
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
        exempt_routes=['/simple_status', '/version'],
        exempt_methods=['HEAD']
    )

    api = application = falcon.API(middleware=[stats_middleware, auth_middleware, cors.middleware, ])

else:
    api = application = falcon.API(middleware=[stats_middleware, cors.middleware, ])


# Routes  ###############
# Add routes to skip authentication in common/middleware:AuthMiddleware.skip_routes list

# BEL Language routes
api.add_route('/bel/versions', BelVersions())  # GET
api.add_route('/bel/{version}/specification', BelSpecificationResource())  # GET
api.add_route('/bel/{version}/completion', BelCompletion())  # GET
api.add_route('/bel/{version}/completion/{belstr}', BelCompletion())  # GET
# api.add_route('/bel/{version}/functions', BelSpecificationResource())  # GET
# api.add_route('/bel/{version}/relations', BelSpecificationResource())  # GET

# Term routes
api.add_route('/terms', TermsResource())  # GET
api.add_route('/terms/completions/{completion_text}', TermCompletionsResource())

api.add_route('/terms/{term_id}', TermResource())  # GET
api.add_route('/terms/{term_id}/equivalents', TermEquivalentsResource())  # GET
api.add_route('/terms/{term_id}/canonicalized', TermCanonicalizeResource())  # GET
api.add_route('/terms/{term_id}/decanonicalized', TermDecanonicalizeResource())  # GET
api.add_route('/terms/types', TermTypesResource())  # GET

# Orthology routes
api.add_route('/orthologs', OrthologResource())  # GET
api.add_route('/orthologs/{gene_id}', OrthologResource())  # GET
api.add_route('/orthologs/{gene_id}/{species}', OrthologResource())  # GET

# Text routes
api.add_route('/text/pubmed/{pmid}', PubmedResource())  # GET

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
