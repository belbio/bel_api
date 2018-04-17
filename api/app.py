#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

import falcon
from falcon_cors import CORS
from falcon_auth import FalconAuthMiddleware, JWTAuthBackend

import logging
import logging.config
# from pythonjsonlogger import jsonlogger
import bel.setup_logging

from bel.Config import config
from middleware.stats import FalconStatsMiddleware
from middleware.field_converters import BelConverter

from resources.status import SimpleStatusResource, HealthCheckResource, StatusResource, VersionResource

from resources.bel_lang import BelVersions
from resources.bel_lang import BelSpecificationResource
from resources.bel_lang import BelCompletion
from resources.bel_lang import BelCanonicalize
from resources.bel_lang import BelDecanonicalize

from resources.tasks import PipelineTasksResource
from resources.tasks import ResourcesTasksResource

from resources.edges import EdgeResource
from resources.edges import EdgesResource

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

bel.setup_logging.setup_logging()

log = logging.getLogger('root')

# log = structlog.getLogger(module_fn)

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
        exempt_routes=['/simple_status', '/healthcheck', '/version', ],
        exempt_methods=['HEAD']
    )

    api = application = falcon.API(middleware=[stats_middleware, auth_middleware, cors.middleware, ])

else:
    api = application = falcon.API(middleware=[stats_middleware, cors.middleware, ])

# Router converter for BEL Expressions and NSArgs
#   converts_FORWARDSLASH_ to / after URI template fields are extracted
#
api.router_options.converters['bel'] = BelConverter

# Routes  ###############
# Add routes to skip authentication in common/middleware:AuthMiddleware.skip_routes list

# BEL Language routes
api.add_route('/bel/versions', BelVersions())  # GET
api.add_route('/bel/{version}/specification', BelSpecificationResource())  # GET
api.add_route('/bel/{version}/completion', BelCompletion())  # GET
api.add_route('/bel/{version}/completion/{belstr:bel}', BelCompletion())  # GET
api.add_route('/bel/{version}/canonicalize/{belstr:bel}', BelCanonicalize())  # GET
api.add_route('/bel/{version}/decanonicalize/{belstr:bel}', BelDecanonicalize())  # GET

# api.add_route('/bel/{version}/functions', BelSpecificationResource())  # GET
# api.add_route('/bel/{version}/relations', BelSpecificationResource())  # GET

# EdgeStore routes
api.add_route('/edges/{edge_id}', EdgeResource())  # GET

# Nanopub routes


# Task routes
api.add_route('/tasks/pipeline', PipelineTasksResource())  # POST
api.add_route('/tasks/resources', ResourcesTasksResource())  # POST


# Term routes
api.add_route('/terms', TermsResource())  # GET
api.add_route('/terms/completions/{completion_text:bel}', TermCompletionsResource())

api.add_route('/terms/{term_id:bel}', TermResource())  # GET
api.add_route('/terms/{term_id:bel}/equivalents', TermEquivalentsResource())  # GET
api.add_route('/terms/{term_id:bel}/canonicalized', TermCanonicalizeResource())  # GET
api.add_route('/terms/{term_id:bel}/decanonicalized', TermDecanonicalizeResource())  # GET
api.add_route('/terms/types', TermTypesResource())  # GET

# Orthology routes
api.add_route('/orthologs', OrthologResource())  # GET
api.add_route('/orthologs/{gene_id:bel}', OrthologResource())  # GET
api.add_route('/orthologs/{gene_id:bel}/{species}', OrthologResource())  # GET

# Text routes
api.add_route('/text/pubmed/{pmid}', PubmedResource())  # GET

# Status endpoints - used to check that API is running correctly
api.add_route('/simple_status', SimpleStatusResource())  # GET un-authenticated
api.add_route('/healthcheck', HealthCheckResource())  # GET un-authenticated
api.add_route('/status', StatusResource())  # GET authenticated
api.add_route('/version', VersionResource())  # version

# Useful for debugging problems in your API; works with pdb.set_trace()
if __name__ == '__main__':
    from wsgiref import simple_server

    host = "127.0.0.1"
    port = 8000
    httpd = simple_server.make_server(host, port, api)
    print("Serving on {}:{}".format(host, port))
    httpd.serve_forever()
