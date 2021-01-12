#! /bin/bash

kgtk --debug --progress --progress-tty `tty` \
     cat --verbose \
     --input-files \
     lexicalize-file1-without-qualifiers-all-entity-labels-en.tsv.gz \
     lexicalize-file1-without-qualifiers.tsv.gz \
     / lexicalize --explain --verbose \
     --add-entity-labels-from-input \
     --output-file lexicalize-test3-output.tsv \
     
