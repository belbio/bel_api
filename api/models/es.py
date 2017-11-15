#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Config import config
from elasticsearch import Elasticsearch

import logging
log = logging.getLogger(__name__)

es = Elasticsearch([config.servers.elasticsearch], send_get_body_as='POST')


def index_exists(index):
    """
    Input: index -- index to check for existence

    """
    return es.indices.exists(index=index)


def main():
    pass


if __name__ == '__main__':
    main()
