#! /bin/bash

kgtk --debug --progress \
     unique --input-file lexicalize-file1-without-qualifiers.tsv.gz \
            --column node1 \
            --output-file lexicalize-file1-without-qualifiers-node1-counts.tsv.gz

kgtk --debug --progress \
     unique --input-file lexicalize-file1-without-qualifiers.tsv.gz \
            --column label \
            --output-file lexicalize-file1-without-qualifiers-label-counts.tsv.gz

kgtk --debug --progress \
     unique --input-file lexicalize-file1-without-qualifiers.tsv.gz \
            --column node2 \
            --output-file lexicalize-file1-without-qualifiers-node2-counts.tsv.gz 

kgtk --debug --progress \
     cat -i lexicalize-file1-without-qualifiers-node1-counts.tsv.gz \
            lexicalize-file1-without-qualifiers-label-counts.tsv.gz \
            lexicalize-file1-without-qualifiers-node2-counts.tsv.gz \
            -o lexicalize-file1-without-qualifiers-all-counts.tsv.gz

kgtk --debug --progress \
     ifexists --input-file /data3/rogers/kgtk/gd/kgtk_public_graphs/cache/wikidata-20201130/data/labels.en.tsv.gz \
              --input-keys node1 \
              --filter-file lexicalize-file1-without-qualifiers-all-counts.tsv.gz \
	      --filter-keys node1 \
              --output-file lexicalize-file1-without-qualifiers.labels.en.tsv.gz
               
kgtk --debug --progress \
     lexicalize --explain --verbose \
     --input-file lexicalize-file1-without-qualifiers.tsv.gz --presorted \
     --entity-label-file lexicalize-file1-without-qualifiers.labels.en.tsv.gz \
     --output-file lexicalize-test5-output-explained.tsv.gz

kgtk --debug --progress \
     lexicalize --verbose \
     --input-file lexicalize-file1-without-qualifiers.tsv.gz --presorted \
     --entity-label-file lexicalize-file1-without-qualifiers.labels.en.tsv.gz \
     --output-file lexicalize-test5-output.tsv.gz
