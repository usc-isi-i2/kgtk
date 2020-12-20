#! /bin/bash

kgtk --debug --progress lexicalize --explain --verbose \
     --input-file lexicalize-file1-without-qualifiers.tsv.gz --presorted \
     --output-file lexicalize-test2-output.tsv \
     --entity-label-file lexicalize-file1-without-qualifiers-all-entity-labels-en.tsv.gz \
     
