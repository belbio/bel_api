#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch

from bel_lang.Config import config

import logging
log = logging.getLogger(__name__)

es = Elasticsearch([config['bel_api']['servers']['elasticsearch']], send_get_body_as='POST')


def index_exists(index):
    """
    Input: index -- index to check for existence

    """
    return es.indices.exists(index=index)


def main():
    pass


if __name__ == '__main__':
    main()
