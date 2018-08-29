from middleware.field_converters import BelConverter

from resources.status import SimpleStatusResource, HealthCheckResource, StatusResource, VersionResource
from resources.swagger import SwaggerResource

from resources.bel_lang import BelVersions
from resources.bel_lang import BelSpecificationResource
from resources.bel_lang import BelCompletion
from resources.bel_lang import BelCanonicalize
from resources.bel_lang import BelDecanonicalize

from resources.bel_lang import BelMigrate12

from resources.tasks import PipelineTasksResource
from resources.tasks import ResourcesTasksResource

from resources.nanopubs import NanopubValidateResource

from resources.edges import EdgeResource
from resources.edges import EdgesFromNanopubResource

from resources.terms import TermResource
from resources.terms import TermsResource
from resources.terms import TermCompletionsResource
from resources.terms import TermEquivalentsResource
from resources.terms import TermCanonicalizeResource
from resources.terms import TermDecanonicalizeResource
from resources.terms import TermTypesResource

from resources.orthology import OrthologResource

from resources.belspec import BelSpecResource

from resources.pubmed import PubmedResource


def add_routes(api):
    # Router converter for BEL Expressions and NSArgs
    #   converts_FORWARDSLASH_ to / after URI template fields are extracted
    #
    api.router_options.converters['bel'] = BelConverter

    # Routes  ###############
    # Add routes to skip authentication in common/middleware:AuthMiddleware.skip_routes list

    # BEL Language routes
    api.add_route('/bel/versions', BelVersions())  # GET
    api.add_route('/bel/{version}/completion', BelCompletion())  # GET
    api.add_route('/bel/{version}/completion/{belstr:bel}', BelCompletion())  # GET
    api.add_route('/bel/{version}/canonicalize/{belstr:bel}', BelCanonicalize())  # GET
    api.add_route('/bel/{version}/decanonicalize/{belstr:bel}', BelDecanonicalize())  # GET

    # BEL1->2 Migration
    api.add_route('/bel/migrate12/{belstr:bel}', BelMigrate12())  # GET

    # api.add_route('/bel/{version}/functions', BelSpecificationResource())  # GET
    # api.add_route('/bel/{version}/relations', BelSpecificationResource())  # GET

    # Edges and EdgeStore
    api.add_route('/edges/{edge_id}', EdgeResource())  # GET
    api.add_route('/edges/nanopub/', EdgesFromNanopubResource())  # GET

    # Nanopub routes
    api.add_route('/nanopubs/validate', NanopubValidateResource())  # POST

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

    # BEL Specification routes
    api.add_route('/belspec', BelSpecResource())  # GET listing, PUT update
    api.add_route('/belspec/{version}', BelSpecResource())  # GET, PUT,  DELETE

    # Text routes
    api.add_route('/text/pubmed/{pmid}', PubmedResource())  # GET

    # Status endpoints - used to check that API is running correctly
    api.add_route('/simple_status', SimpleStatusResource())  # GET un-authenticated
    api.add_route('/healthcheck', HealthCheckResource())  # GET un-authenticated
    api.add_route('/status', StatusResource())  # GET authenticated
    api.add_route('/version', VersionResource())  # version
    api.add_route('/swagger', SwaggerResource())
