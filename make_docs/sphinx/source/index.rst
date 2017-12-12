.. BEL.bio API documentation master file, created by
   sphinx-quickstart on Mon Dec 11 15:42:18 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

BEL.bio API Docs
=======================================

The BEL.bio API provides a REST API for the BEL Language and BEL Content.

Functionality provided:

-  BEL Namespace queries
-  BEL language parsing and validation [TODO]
-  BEL Nanopub management and validation [TODO]
-  BEL Edge creation from BEL Nanopubs [TODO]
-  BEL EdgeStore services [TODO]

.. _BEL.bio: http://bel.bio
.. _BEL: http://openbel.org/language/version_2.0/bel_specification_version_2.0.html

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   API Reference (Swagger) <http://apidocs.bel.bio/openapi/index.html>
   glossary
   requirements
   related
   link_contributing
   link_conduct

Background
-------------

`BEL.bio`_ is a clean build of a BEL_ platform using Python 3.6+ and Docker to
increase ease of community use and deployment. Some major enhancements are:

- Supports multiple versions of BEL at the same time
- Improved syntactic and semantic validation over OpenBEL API
- Ability to manage BEL Namespaces individually
- Elasticsearch based namespace searching and term completion
- Python libraries designed to support BEL statement, nanopub, edge parsing






Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
