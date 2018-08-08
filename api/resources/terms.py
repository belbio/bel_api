import falcon
import services.terms as terms
import json
import fastcache

import logging
log = logging.getLogger(__name__)


class TermResource(object):
    """Term endpoint"""

    @fastcache.clru_cache(maxsize=500)
    def on_get(self, req, resp, term_id=None):
        """GET Term using term_id

        This will return the record if it finds the term_id in the
        id field or the alt_ids field.
        """

        if term_id is None:
            resp.media = {'title': 'Term endpoint Error', 'message': 'Must provide a term id, e.g. /term/HGNC:AKT1'}
            resp.status = falcon.HTTP_200
            return

        term = terms.get_term(term_id)
        if term:
            resp.media = term
            resp.status = falcon.HTTP_200
        else:
            description = 'No term found for {}'.format(term_id)
            resp.media = {'title': 'No Term', 'message': description}
            resp.status = falcon.HTTP_404


class TermsResource(object):

    """Get Users listing based on query - generally by organization

    create new
    """

    def on_get(self, req, resp):
        """GET List of Terms

            Results:
                List[Mapping[str, Any]]: list of terms
        """
        resp.media = {'title': 'Terms GET query', 'message': 'To be implemented.'}
        resp.status = falcon.HTTP_200


class TermEquivalentsResource(object):
    """User Profile"""

    def on_get(self, req, resp, term_id):
        """GET User Profile"""

        results = terms.get_equivalents(term_id)
        resp.media = {'equivalents': results}
        resp.status = falcon.HTTP_200


class TermCanonicalizeResource(object):
    """User Profile"""

    def on_get(self, req, resp, term_id):
        """GET User Profile"""

        namespace_targets = req.get_param('namespace_targets')
        if namespace_targets:
            namespace_targets = json.loads(namespace_targets)
        term_id = terms.canonicalize(term_id, namespace_targets=namespace_targets)
        resp.media = {'term_id': term_id}
        resp.status = falcon.HTTP_200


class TermDecanonicalizeResource(object):
    """User Profile"""

    def on_get(self, req, resp, term_id):
        """GET User Profile"""

        namespace_targets = req.get_param('namespace_targets')
        if namespace_targets:
            namespace_targets = json.loads(namespace_targets)

        term_id = terms.decanonicalize(term_id)
        resp.media = {'term_id': term_id}
        resp.status = falcon.HTTP_200


class TermCompletionsResource(object):

    """Get NSArgs that match completion request"""

    def on_get(self, req, resp, completion_text):
        """GET List of Terms

            Args:
                completion_text (str): partial term or term description to search for - may be null

            Results:
                List[Mapping[str, Any]]: list of terms
        """

        size = req.get_param('size', default=21)
        entity_types = req.get_param('entity_types', [])
        species = req.get_param('species_id', req.get_param('species', []))
        annotation_types = req.get_param('annotation_types', [])
        namespaces = req.get_param('namespaces', [])

        completions = terms.get_term_completions(completion_text, size, entity_types, annotation_types, species, namespaces)
        resp.media = {'completion_text': completion_text, 'completions': completions}
        resp.status = falcon.HTTP_200


class TermTypesResource(object):
    """Get Namespaces, Entity Types, and Context Types in TermStore

    Get facet counts for each (top 100 for each)
    """

    @fastcache.clru_cache(maxsize=500)
    def on_get(self, req, resp):
        """ Get stats """

        resp.media = terms.term_types()
        resp.status = falcon.HTTP_200


