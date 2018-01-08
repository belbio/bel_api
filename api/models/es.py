#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bel.db.elasticsearch

import logging
log = logging.getLogger(__name__)

es = bel.db.elasticsearch.get_client()


def index_exists(index):
    """
    Input: index -- index to check for existence

    """
    return es.indices.exists(index=index)


def main():
    pass


if __name__ == '__main__':
    main()
