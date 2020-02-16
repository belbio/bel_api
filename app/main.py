#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

import bel.lang.bel_specification
# import logging
# import logging.config
# # from pythonjsonlogger import jsonlogger
import bel.setup_logging
import falcon
import gevent.monkey
# TODO - figure out how to run logging setup and belspec once on startup rather than
#        every time a worker is initialized (moved bel.lang.bel_specification.update_specifications to bel/__init__.py)
import structlog
from bel.Config import config
from falcon_auth import FalconAuthMiddleware, JWTAuthBackend
from falcon_cors import CORS

import middleware.falcon_exceptions
import services.swaggerui
from middleware.field_converters import BelConverter
from middleware.stats import FalconStatsMiddleware
from resources.bel_lang import (BelCanonicalize, BelCompletion,
                                BelDecanonicalize, BelMigrate12,
                                BelSpecificationResource, BelVersions)
from resources.belspec import BelSpecResource
from resources.nanopubs import NanopubValidateResource
from resources.orthology import OrthologResource
from resources.pubmed import PubmedResource
from resources.status import (HealthCheckResource, PingResource,
                              SimpleStatusResource, StatusResource,
                              VersionResource)
from resources.swagger import SwaggerResource
from resources.tasks import ResourcesTasksResource
from resources.terms import (TermCanonicalizeResource, TermCompletionsResource,
                             TermDecanonicalizeResource,
                             TermEquivalentsResource, TermResource,
                             TermsResource, TermTypesResource)

gevent.monkey.patch_all()


# Setup logging
module_fn = os.path.basename(__file__)
module_fn = module_fn.replace(".py", "")

log = structlog.getLogger("bel_api")

cors = CORS(
    allow_all_origins=True,
    allow_all_methods=True,
    allow_all_headers=True,
    allow_credentials_all_origins=True,
)

stats_middleware = FalconStatsMiddleware()

# Allow requiring authentication via JWT
if config["bel_api"]["authenticated"]:

    # Loads user data from JWT
    def user_loader(payload):
        # log.info(payload)
        return True

    auth_backend = JWTAuthBackend(
        user_loader=user_loader,
        secret_key=config["secrets"]["bel_api"]["shared_secret"],
        required_claims=["exp", "iat"],
    )
    auth_middleware = FalconAuthMiddleware(
        auth_backend,
        exempt_routes=["/simple_status", "/healthcheck", "/version"],
        exempt_methods=["HEAD"],
    )

    app = application = falcon.API(middleware=[stats_middleware, auth_middleware, cors.middleware])

else:
    app = application = falcon.API(middleware=[stats_middleware, cors.middleware])

# Add exception handling
middleware.falcon_exceptions.register_defaults(app)

# Add Swagger UI
services.swaggerui.register_swaggerui(app)


# Router converter for BEL Expressions and NSArgs
#   converts_FORWARDSLASH_ to / after URI template fields are extracted
#
app.router_options.converters["bel"] = BelConverter

# Routes  ###############
# Add routes to skip authentication in common/middleware:AuthMiddleware.skip_routes list

# BEL Language routes
app.add_route("/bel/versions", BelVersions())  # GET
app.add_route("/bel/{version}/specification", BelSpecificationResource())  # GET
app.add_route("/bel/{version}/completion", BelCompletion())  # GET
app.add_route("/bel/{version}/completion/{belstr:bel}", BelCompletion())  # GET
app.add_route("/bel/{version}/canonicalize/{belstr:bel}", BelCanonicalize())  # GET
app.add_route("/bel/{version}/decanonicalize/{belstr:bel}", BelDecanonicalize())  # GET

# BEL1->2 Migration
app.add_route("/bel/migrate12/{belstr:bel}", BelMigrate12())  # GET

# app.add_route('/bel/{version}/functions', BelSpecificationResource())  # GET
# app.add_route('/bel/{version}/relations', BelSpecificationResource())  # GET

# Nanopub routes
app.add_route("/nanopubs/validate", NanopubValidateResource())  # POST

# Task routes
app.add_route("/tasks/resources", ResourcesTasksResource())  # POST


# Term routes
app.add_route("/terms", TermsResource())  # GET
app.add_route("/terms/completions/{completion_text:bel}", TermCompletionsResource())

app.add_route("/terms/{term_id:bel}", TermResource())  # GET
app.add_route("/terms/{term_id:bel}/equivalents", TermEquivalentsResource())  # GET
app.add_route("/terms/{term_id:bel}/canonicalized", TermCanonicalizeResource())  # GET
app.add_route("/terms/{term_id:bel}/decanonicalized", TermDecanonicalizeResource())  # GET
app.add_route("/terms/types", TermTypesResource())  # GET

# Orthology routes
app.add_route("/orthologs", OrthologResource())  # GET
app.add_route("/orthologs/{gene_id:bel}", OrthologResource())  # GET
app.add_route("/orthologs/{gene_id:bel}/{species}", OrthologResource())  # GET

# BEL Specification routes
app.add_route("/belspec", BelSpecResource())  # GET, PUT
app.add_route("/belspec/{version}", BelSpecResource())  # GET, DELETE

# Text routes
app.add_route("/text/pubmed/{pmid}", PubmedResource())  # GET

# Status endpoints - used to check that app is running correctly
app.add_route("/simple_status", SimpleStatusResource())  # GET un-authenticated
app.add_route("/healthcheck", HealthCheckResource())  # GET un-authenticated
app.add_route("/status", StatusResource())  # GET authenticated
app.add_route("/version", VersionResource())  # version
app.add_route("/swagger", SwaggerResource())
app.add_route("/ping", PingResource())

# Useful for debugging problems in your app; works with pdb.set_trace()
if __name__ == "__main__":
    from wsgiref import simple_server

    host = "127.0.0.1"
    port = 8181
    httpd = simple_server.make_server(host, port, app)
    print("Serving on {}:{}".format(host, port))
    httpd.serve_forever()
