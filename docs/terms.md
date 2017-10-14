# Terminology and Orthology Processing

**TODO: Add Makefile and config file to manage collecting terms, orthologs and updating elasticsearch and arangodb**

## Overview

1. Run the Terminology script (for download and source file processing) to generate each Terminology \<term\>.jsonl.gz files
    1. First Download Original Term database files and compress using gzip
        1. If it is newer than prior download if determinable (some FTP servers
        don't make filedates available)
        1. If source filedates indeterminable, download is local file is older than
        7 days - this is adjustable to longer per term source
    1. Terminology script then processes the original source files to create the term data, equivalence and hierarchy
    1. Terminology script writes out each term into a gzipped [JSONL](http://jsonlines.org) file.
1. Run elasticsearch load script to upload each \<term\>.jsonl.gz file to Elasticsearch (after initially setting up the Elasticsearch terms index).
1. Generate equivalence files to load into ArangoDB from \<term\>.jsonl.gz files
1. Load equivalence files into ArangoDB.
1. Run Orthology scripts
1. First Download Original Orthology database files and compress using gzip
        1. If it is newer than prior download if determinable (some FTP servers
        don't make filedates available) (orthology and terminology source files use same download location so will only download once if used by both
        terminology and orthology scripts)
        1. If source filedates indeterminable, download is local file is older than
        7 days - this is adjustable to longer per term source
    1. Orthology script then processes the original source files to create the orthologous relationships
    1. Terminology script writes out each term into a gzipped [JSONL](http://jsonlines.org) file.
1. Load orthology datasets into ArangoDB


## Terminology Scripts

Each terminology script is an independent script. Most do utilize some utility
functions from a utility library supporting the terminology and orthology scripts.

Generally the terminology scripts do two main things:

1. Download the terminology source datafiles
1. Build the \<term\>.jsonl.gz file

All of the terminology scripts will be stored in the resource_tools/terms directory.  Any \*.py files in that directory will be run to (re-)create the \<term\>.jsonl.gz files.  The terminology scripts will create the \<term\>.jsonl.gz files in the resource_tools/data/terms directory. Any \*.jsonl.gz files will be loaded into Elasticsearch into the terms index.

## Taxonomy Terminology

Taxonomy IDs are based on the [NCBI Taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy). Taxonomy is treated just like other terminologies with additional features of taxonomy_name object and taxonomy_rank (kingdom, ..., genus, species).  **The Taxonomy terminology script has to be run first as it creates the taxonomy_labels.json.gz file which is used by all terminologies that stores species_id and species_label in the \<term\>.jsonl.gz files**.

The taxonomy_labels.json.gz file is a map (dictionary/hash) of all of the TAX:\<int\> versus labels but only for taxonomy entries with taxonomy_rank: "species".  **Note: It may be necessary to add labels to this file for entries with non-species taxonomy_rank as several EntrezGene and SwissProt namespace entries do not have labels in this file.**

The Taxonomy Namespace prefix is 'TAX'.  Humans have the taxonomy id of TAX:9606 with a custom label of 'human'.

Custom labels for specific species are sourced from the *taxonomy_labels.yaml* file adjacent to the taxonomy.py terminology script.  Custom labels file looks like:

    # Override taxonomy label
    # taxonomy_src_id: label
    ---
    9606: human
    10090: mouse
    10116: rat
    7955: zebrafish


## Orthology Scripts

Orthology Gene/Protein IDs collected from their source files need to be converted to the canonical Namespace for Genes/Proteins (currently Entrez Gene, prefix EG) prior to loading into ArangoDB **TODO**.  This will save time in processing through the equivalence edges.


## Terminology and Orthology Schemas

Schemas for terminologies and orthologies are kept in the [BELBio Schema Repository](https://github.com/belbio/schemas/tree/master/schemas).


## Elasticsearch Index

The Elasticsearch index map is in the es_mapping_term.yaml file and the index is created using the setup_es.py script.  This setup_es.py script must be run before loading the terminologies the first time.  It will delete the *terms* index if it already exists. **Note: Need to setup an A/B index option so that we can switch the index alias to a new terms index.**


## ArangoDB

A 'bel' database is created and the following collections are added and loaded:

1. ortholog_nodes
1. ortholog_edges
1. equivalence_nodes
1. equivalence_edges

These collections of nodes and edges allow equivalence and orthology queries to be run against the bel ArangoDB database.
