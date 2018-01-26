Glossary
------------

.. glossary::

    API
        BEL.bio API – BEL language, BEL Nanopub, BEL Namespaces (and equivalences and orthology) and BEL Edge REST API services

    Argument

        An Argument is a BEL function argument which may be another BEL function, a BEL entity, or a BEL function modifier

            act(p(HGNC:VHL)) directlyIncreases deg(p(HGNC:HIF1A)) -- the 'act' function has a BEL function as a parameter p()

            p(HGNC:AKT1,pmod(P,T,308)) -- the p() function has a BEL entity (HGNC:AKT1) and a pmod() function modifier

    AST
        Abstract Syntax Tree of BEL Assertion or BEL Triple. A hierarchically organized data structure of the BEL Assertion which is very useful for performing transforms such as canonicalization, orthologization or generating computed edges.

    AST Function
        BEL function, e.g. p() or modifier function, e.g. var()

    AST NSArg or NSArg
        Namespace argument, e.g. p(HGNC:AKT1), HGNC:AKT1 is the namespace argument where HGNC is the namespace prefix and AKT1 is the Namespace value.

    AST StrArg or StrArg
        String argument, e.g. pmod(Ph, T, 22), Ph, T and 22 are string arguments.

    BEL
        BEL stands for Biological Expression Language. BEL is a means of capturing biological knowledge in a manner that is human friendly and convertible into computable formats for supporting knowledge-driven analytics. It also serves as a format to share biological knowledge using an open standard.

    BEL Assertion
        The key assertion(s) being made in a BEL Nanopub. It is an expression that represents knowledge of the existence of biological entities and relationships between them that are known to be observed within a particular experiment context (i.e. Experiment Context), based on some source of prior knowledge such as a scientific publication or newly generated experimental data.

        It can also refer to the single string version of a BEL triple (combining the subject, relation and object of a BEL triple).

    BEL Edge
        BEL triples, computed BEL canonicalized to standard BEL Namespace IDs and potentially orthologized which are stored in an EdgeStore (a graph database).

    BEL Entity

        A BEL entity is a biological/chemical entity or concept found as a parameter of a BEL function. The BEL entity may be composed of a BEL namespace and an identifier, but it does not have to have a namespace which may lead to an ambiguous identifier for the BEL entity. Example BEL entity: HGNC:AKT1 which is the AKT1 identifier in the HGNC namespace (Human Gene Nomenclature Committee).

    BEL Namespaces
        A terminology used to unambiguously identify a gene/protein, biological process, pathology, cell line, etc. The terms in BEL Namespace have a namespace prefix such as **HGNC** for Human Gene Nomenclature Committee human gene symbols or GO for Gene Ontology. The Namespace definition may contain equivalents to other namespaces; it may also contain hierarchical structure such as an Anatomy namespace or the Gene Ontology.

    BEL Nanopub

        A Nanopub is defined by http://nanopub.org. Quoting their definition:

            A nanopublication is the smallest unit of publishable information: an assertion about anything that can be uniquely identified and attributed to its author.

            Individual nanopublications can be cited by others and tracked for their impact on the community.

            Nanopublications are a natural response to the explosion of high-quality contextual information that overwhelms the capacity of conventional research articles in scholarly communication.

        A BEL Nanopub is an atomic instance of BEL knowledge to represent a biological interaction or fact with an experimental context and provenance. A BEL Nanopub consists of the following parts:

        *Citation*

        The identification of the scientific literature or database where the interaction was originally asserted.

        *BEL Assertion*

        The biological interaction curated from the Citation.

        *Evidence*

        Extracted text that supports the BEL Assertion. For example, this may be a text quotation, or link to a figure, or table within the Citation. This has been through some name changes (called 'Evidence' and 'Support' in BEL Scripts and 'Support' in OpenBEL Nanopub format).

        *Annotations*

        The biological context within the experiment where the BEL Statement is observed. For example, if the experiment sample was a biopsy on Human, Lung tissue then you might provide an Annotation of Ncbi Taxonomy with value Homo sapiens and Uberon with value lung epithelium. Additional annotations may be included such as actual gene expression values or timepoints.

        Annotations are a managed as a list of (AnnotationType, ID and label).  The AnnotationType indicates what type of annotation it is such as Species, Disease, CellLine, etc.  The Annotation ID is now managed as a BEL Namespace which will allow for hierarchical queries in the future.

        *Metadata*

        Additional data about the Nanopub itself. For example if the Nanopub was curated using a text mining approach we may provide a CurationMethod Annotation with value Text Mining.

    BEL Network
        A subset of the BEL Edges in the EdgeStore that are selected for connectivity and environmental context, e.g. BEL Edges connected to p(HGNC:EGFR) for lung cancer in humans.

    BEL Triple
        Discrete Subject, Relation, Object (SRO) version of BEL assertion

    Edge
        See BEL Edge

    EdgeStore
        A database for storing BEL Edges which is search-able via the BEL.bio API. This is a graph database which allows for network neighborhood and shortest path queries between nodes.

    Namespaces
        see BEL Namespaces

    NanopubStore
        A database for storing Nanopubs with a separate CRUD REST API interface and some basic Web Administration.

    Nested BEL Assertion
        Where the object of a BEL triple is another BEL triple, e.g. *subject relation (subject relation object)*.

    NetworkStore
        A database for Networks with a separate CRUD REST API interface and some basic Web Administration.


