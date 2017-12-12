Glossary
------------

.. glossary::

    BEL statement
        single string version of BEL triple

    Nested BEL statement
        Where the object of a BEL triple is another bel triple, e.g. *subject relation (subject relation object)*.

    BEL triple
        subject, relation, object (SRO) version of BEL statement

    BEL Nanopub
        JSON or YAML document containing BEL triple(s), Evidence, Context, Citation, and Metadata

    Evidence
        short text extraction or supporting information for BEL Triple (Evidence in BEL Script, Support in OpenBEL Nanopub format)

    BEL Namespace
        A terminology used to unambiguously identify a gene/protein, biological process, pathology, cell line, etc. The terms in BEL Namespace have a namespace prefix such as **HGNC** for Human Gene Nomenclature Committee human gene symbols or GO for Gene Ontology. The Namespace definition may contain equivalents to other namespaces; it may also contain hierarchical structure such as an Anatomy namespace or the Gene Ontology.

    Context
        OpenBEL Annotations are now called Context and referred to as *Experimental Context* in BELMgr.  Context is a list of (context_type, ID and label).  The context_type indicates what type of context it is such as Species, Disease, CellLine, etc.  The context id is now managed as a BEL Namespace which will allow for hierarchical queries in the future.

    BEL Edge
        BEL triples, computed BEL canonicalized to standard BEL Namespace IDs and potentially orthologized stored in EdgeStore (a graph database)

    API
        BEL.bio API – BEL language, BEL Nanopub, terminology (BEL Namespaces, equivalences and orthology) and BEL Edge REST API services

    AST
        Abstract Syntax Tree of BEL Statement or BEL Triple

    AST Function
        BEL function, e.g. p() or modifier function, e.g. var()

    AST NSArg or NSArg
        Namespace argument, e.g. HGNC:AKT1, Namespace prefix plus namespace value

    AST StrArg or StrArg
        String argument, e.g. pmod(Ph, T, 22), Ph, T and 22 are string arguments
