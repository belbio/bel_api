# BEL.bio API

The BEL.bio API provides a REST API for the BEL Language and platform services for using the BEL
Language and BEL Content.

Functionality [to be] provided:

- BEL Namespaces and Orthology services
- BEL Language parsing and validation [in process]
- BEL Statement completion [in process]
- BEL Nanopub management and validation [in process]
- BEL Edge creation from BEL Nanopubs [not started]
- BEL EdgeStore services [not started]

`Project Documentation <http://apidocs.bel.bio/>`

- OpenAPI/Swagger API documentation
- Quick start
- Contributing guidelines
- and more

`DockerHub BEL.bio API image <https://hub.docker.com/r/belbio/bel_api/>`

## Development

The Makefile will build the pipeline image and deploy it to Dev.

WARNING: This copies the watchexec rsync'd (see manage servers bin/sync_bel.sh) bel repo using the
Dockerfile.dev into the image.

The Dockerfile.prod uses a specific branch on github for _bel_.
