#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import falcon

from Config import config  # Application settings enabled for Dev/Test/Prod

from common.middleware import AuthMiddleware, RequireJSON, JSONTranslator
from resources.status import SimpleStatusResource, StatusResource

from services.custom_logger import setup_custom_logger
logger = setup_custom_logger('root')
logger.setLevel(config['log_level'])

api = application = falcon.API(middleware=[AuthMiddleware(), RequireJSON(), JSONTranslator(), ])

# Routes  ###############
# Add routes to skip authentication in common/middleware:AuthMiddleware.skip_routes list

# Status endpoints - used to check that API is running correctly
api.add_route('/simple-status', SimpleStatusResource())  # un-authenticated
api.add_route('/status', StatusResource())  # authenticated

# Useful for debugging problems in your API; works with pdb.set_trace()
if __name__ == '__main__':
    from wsgiref import simple_server

    host = "127.0.0.1"
    port = 8000
    httpd = simple_server.make_server(host, port, api)
    print("Serving on {}:{}".format(host, port))
    httpd.serve_forever()
