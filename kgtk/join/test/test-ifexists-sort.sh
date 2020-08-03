kgtk ifexists \
     examples/sample_data/aida/HC00001DO.ttl.unreified.nojust.tsv \
     --output-file HC00001DO.entities-unsorted.tsv \
     --input-keys node1 \
     --filter-keys node1 \
     --filter-on examples/sample_data/aida/HC00001DO.entity_ids.tsv \


kgtk sort HC00001DO.entities-unsorted.tsv  --columns 1,2 \
   > HC00001DO.entities.tsv

kgtk sort HC00001DO.entities-unsorted.tsv  --columns 1,2 > HC00001DO.entities.tsv

kgtk ifexists \
     examples/sample_data/aida/HC00001DO.ttl.unreified.nojust.tsv \
     --output-file HC00001DO.entities-unsorted.tsv \
     --input-keys node1 \
     --filter-keys node1 \
     --filter-on examples/sample_data/aida/HC00001DO.entity_ids.tsv \
   / sort --columns 1,2 \
   > HC00001DO.entities.tsv


kgtk cat HC00001DO.entities-unsorted.tsv \
   / sort --columns 1,2 \
   > HC00001DO.entities.tsv
	   
kgtk cat HC00001DO.entities-unsorted.tsv 

kgtk cat HC00001DO.entities-unsorted.tsv / sort --columns 1,2  > HC00001DO.entities.tsv

pv HC00001DO.entities-unsorted.tsv | kgtk sort --columns 1,2  > HC00001DO.entities.tsv
	   
kgtk cat HC00001DO.entities-unsorted.tsv / cat -o xxx.tsv


kgtk cat HC00001DO.entities-unsorted.tsv / cat > xxx.txv

kgtk cat HC00001DO.entities-unsorted.tsv / sort - --columns 1,2  > HC00001DO.entities.tsv
kgtk cat HC00001DO.entities-unsorted.tsv / sort -i - --columns 1,2  > HC00001DO.entities.tsv

kgtk cat HC00001DO.entities-unsorted.tsv / sort --columns 1,2  -o HC00001DO.entities.tsv


kgtk import-ntriples \
     -i examples/sample_data/aida/HC00001DO.ttl.nt \
     --namespace-file examples/sample_data/aida/aida-namespaces.tsv \
     --namespace-id-use-uuid True \
     --local-namespace-use-uuid False \
     --local-namespace-prefix _ \
     --newnode-use-uuid True  \
     --output-file xxx.tsv

kgtk import-ntriples \
     -i examples/sample_data/aida/HC00001DO.ttl.nt \
     --namespace-file examples/sample_data/aida/aida-namespaces.tsv \
     --namespace-id-use-uuid True \
     --local-namespace-use-uuid False \
     --local-namespace-prefix _ \
     --newnode-use-uuid True  \
     / sort \
     --out xxx.tsv
