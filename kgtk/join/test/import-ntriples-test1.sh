#! /bin/bash

kgtk import_ntriples \
     -i ../../HC00001DO.ttl.nt \
     -o HC00001DO.tsv \
     --reject-file HC00001DO-rejects.ttl.nt \
     --namespace-file kgtk/join/test/initial-ntriple-namespaces.tsv \
     --updated-namespace-file HC00001DO-namespaces.tsv \
     --namespace-id-use-uuid True \
     --newnode-use-uuid True \
     
