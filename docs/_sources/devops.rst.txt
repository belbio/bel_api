DevOps
===========

All administrative tasks are managed by running make tasks using the top-level Makefile in the project folder.

Builds and Testing
--------------------

We will use TravisCI for Open Source to run builds and tests.

Documentation
----------------

We use OpenAPI (Swagger) for the API documentation.  Due to having to host the SwaggerUI code, we keep the documentation source in `bel_api/make_docs` to hold both the SwaggerUI and Sphinx source.  The generated documentation is created in `bel_api/docs` which is deployed using Github Pages.


Dependabot
--------------

We use https://app.dependabot.com/accounts/belbio/repos to keep the
python module requirements up to date.  It uses the `belbio` user id.


Code Quality
-------------------

We are using Code Climate for code quality assessments.

We are using CodeCov for code test coverage assessments.

Contributor Licensing Agreements
--------------------------------------

All pull requests require signing the [CLA Assistant](https://cla-assistant.io/) Contributor's License Agreement.
