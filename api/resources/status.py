import falcon


class SimpleStatusResource(object):
    """Simple status - un-authenticated endpoint"""

    def on_get(self, req, resp):

        resp.body = '{"profile": "Simple Status API Endpoint works"}\n'
        resp.status = falcon.HTTP_200


class StatusResource(object):
    """Status endpoint - authenticated"""

    def on_get(self, req, resp):

        resp.body = '{"profile": "Test API Endpoint works "}\n'
        resp.status = falcon.HTTP_200

        # TODO dump out all configuration except secrets with Status endpoint
