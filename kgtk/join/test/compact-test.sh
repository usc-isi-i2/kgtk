kgtk connected_components --properties mw:SameAs \
    --input-file kgtk/join/test/compact-file6.tsv \
    --output-file connected.tsv

kgtk lift --columns-to-lift node1 node2 --lift-suffix= \
     --input-file kgtk/join/test/compact-file6.tsv \
     --output-file lifted.tsv \
     --label-file connected.tsv \
     --label-select-value connected_component

kgtk filter --invert -p ';mw:SameAs;' \
     --input-file lifted.tsv \
     --output-file filtered.tsv

kgtk compact --columns node1 relation node2 --compact-id \
     --input-file filtered.tsv \
     --output-file output.tsv
