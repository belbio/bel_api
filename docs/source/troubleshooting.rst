Troubleshooting
-----------------

.. toctree::
   :maxdepth: 1
   :caption: Contents:

Results not up to date
-------------------------------

.. note::
    Caching REST API Requests to external servers including Elasticsearch and ArangoDB using Requests CacheControl up to 1 day.

This means that terms, orthologies, pubmed content, etc is cached and may be stale. This can be reset by restarting the BEL.bio API server.
