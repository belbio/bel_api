Glossary
------------

Organized by importance of term not alphabetically

.. glossary::

    BEL assertion
        single string version of a BEL triple

    Nested BEL assertion
        Where the object of a BEL triple is another BEL triple, e.g. *subject relation (subject relation object)*.

    BEL triple
        subject, relation, object (SRO) version of BEL assertion

    BEL Nanopub
        JSON or YAML document containing BEL triple(s), Evidence, Annotations, Citation, and Nanopub Metadata

    BEL Edge
        BEL triples, computed BEL canonicalized to standard BEL Namespace IDs and potentially orthologized which are stored in an EdgeStore (a graph database).

    BEL Network
        A subset of the BEL Edges in the EdgeStore that are selected for connectivity and environmental context, e.g. BEL Edges connected to p(HGNC:EGFR) for lung cancer in humans.

    NanopubStore
        A database for storing Nanopubs with a separate CRUD REST API interface and some basic Web Administration.

    EdgeStore
        A database for storing BEL Edges which is search-able via the BEL.bio API. This is a graph database which allows for network neighborhood and shortest path queries between nodes.

    NetworkStore
        A database for Networks with a separate CRUD REST API interface and some basic Web Administration.

    Evidence
        short text extraction or supporting information for BEL Triple (Evidence in BEL Script, Support in OpenBEL Nanopub format)

    BEL Namespace
        A terminology used to unambiguously identify a gene/protein, biological process, pathology, cell line, etc. The terms in BEL Namespace have a namespace prefix such as **HGNC** for Human Gene Nomenclature Committee human gene symbols or GO for Gene Ontology. The Namespace definition may contain equivalents to other namespaces; it may also contain hierarchical structure such as an Anatomy namespace or the Gene Ontology.

    Annotations
         Annotations are a list of (AnnotationType, ID and label).  The AnnotationType indicates what type of annotation it is such as Species, Disease, CellLine, etc.  The Annotation ID is now managed as a BEL Namespace which will allow for hierarchical queries in the future.

    API
        BEL.bio API – BEL language, BEL Nanopub, BEL Namespaces (and equivalences and orthology) and BEL Edge REST API services

    AST
        Abstract Syntax Tree of BEL Assertion or BEL Triple. A hierarchically organized data structure of the BEL Assertion which is very useful for performing transforms such as canonicalization, orthologization or generating computed edges.

    AST Function
        BEL function, e.g. p() or modifier function, e.g. var()

    AST NSArg or NSArg
        Namespace argument, e.g. p(HGNC:AKT1), HGNC:AKT1 is the namespace argument where HGNC is the namespace prefix and AKT1 is the Namespace value.

    AST StrArg or StrArg
        String argument, e.g. pmod(Ph, T, 22), Ph, T and 22 are string arguments.

