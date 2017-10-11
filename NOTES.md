# BEL API Notes

## API

BEL API GET endpoints (draft):

    query param ast=1 will result in AST returned instead of flattened edges as strings
    /bel/triple/<subject>/<relationship>/<object>/validation
    /bel/triple/<subject>/<relationship>/<object>/canonicalization?namespace_targets={'HGNC': ['EG', 'SP'], ...}
    /bel/triple/<subject>/<relationship>/<object>/orthologization?species=TAXID:10090
    /bel/triple/<subject>/<relationship>/<object>/edges?types=[]  # returns computed edges, filtered by types
    /bel/statement/<stmt>/triple
    /bel/statement/<stmt>/validation
    /bel/statement/<stmt>/canonicalization?namespace_targets={'HGNC': ['EG', 'SP'], ...}
    /bel/statement/<stmt>/orthologization?species=TAXID:10090
    /bel/statement/<stmt>/edges?types=[]

    /terms/<partial_term>
    /term/<term>/validate
    /term/<term>/equivalences?namespaces=['HGNC', 'SP']

    /orthology/<gene>?species=TAXID:10090

## Terminology Service

Define JSON schema for terms

Terms packaged together as JSON Lines or JSON Array

Term header object
* Termset name
* Updated On
* Number of Terms
* URI template
* PREFIX

Term object
* Term id
* Term preferred term - string
* Term label
* Term definition
* Term synonyms - array
* Term parent IDs - array
* Domains - disease, chemical, etc
* Orthologies (optional)
