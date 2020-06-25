#! /bin/bash

kgtk add_id --id-style=empty HC00001DO.tsv -o HC00001DO-with-id.tsv
kgtk unreify_rdf_statements -i HC00001DO-with-id.tsv --trigger-label=XXX -o HC00001DO-with-id-sorted.tsv
kgtk unreify_rdf_statements -i HC00001DO-with-id-sorted.tsv -o HC00001DO-with-id-sorted-unreified.tsv
diff HC00001DO-with-id-sorted.tsv HC00001DO-with-id-sorted-unreified.tsv
