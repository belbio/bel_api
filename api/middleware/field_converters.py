import falcon.routing.converters

import logging
log = logging.getLogger(__name__)


class BelConverter(falcon.routing.converters.BaseConverter):
    """Convert BEL path parameter"""

    def convert(self, value):
        return value.replace('_FORWARDSLASH_', '/')
