#! /bin/bash

kgtk import_ntriples --verbose \
     -i kgtk/join/test/import-ntriples-file3.ttl.nt \
     -o import-ntriples-file3.tsv \
     --reject-file import-ntriples-file3-rejects.ttl.nt \
     --namespace-file kgtk/join/test/initial-ntriple-namespaces.tsv \
     --updated-namespace-file import-ntriples-file3-namespaces.tsv \
     --namespace-id-use-uuid True \
     --newnode-use-uuid True \
     
