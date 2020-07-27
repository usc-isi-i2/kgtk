#! /bin/bash

kgtk import_ntriples --verbose \
     -i kgtk/join/test/import-ntriples-file2.ttl.nt \
     -o import-ntriples-file2.tsv \
     --reject-file import-ntriples-file2-rejects.ttl.nt \
     --namespace-file kgtk/join/test/initial-ntriple-namespaces.tsv \
     --updated-namespace-file import-ntriples-file2-namespaces.tsv \
     --namespace-id-use-uuid True \
     --newnode-use-uuid True \
     
