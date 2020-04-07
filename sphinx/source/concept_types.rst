Concept Types
===================

Entity types
-----------------

Used to define BEL Entities - e.g. HGNC:EGF - based on what function it is in g(), r(), p() could be a Gene, RNA or Protein entity. Chemical compounds and any other substance that is not already described by an entity type are Abundance entity types.  The canonical list of entity types are stored in each version of the BEL Specification YAML document.

  - Abundance
  - Protein
  - RNA
  - Micro_RNA
  - Gene
  - Complex
  - BiologicalProcess
  - Pathology
  - Activity
  - Variant
  - ProteinModification
  - AminoAcid
  - Location


Annotation Types
-------------------

These terms are used as the preferred Annotation type in BEL Nanopubs. They provide a broad classification for terms in the various BEL Namespaces.

.. note:
    You can use other Annotation Types as desired or needed for custom Annotations. If it is generally useful, please consider adding it to this list and provide suggestions on how to tag terms in the BEL Namespaces with the Annotation type so it will be provided in Annotation completion suggestions.

- Anatomy
- Cell
- CellLine
- CellStructure
- Pathology
- Species
