kgtk connected_components \
     --properties mw:SameAs \
     --input-file kgtk/join/test/cc-file1.tsv \
     > clusters.tsv

kgtk lift \
     --input-file kgtk/join/test/cc-file1.tsv \
     --output-file merged.tsv \
     --label-file clusters.tsv \
     --columns-to-lift node1 node2 \
     --lift-suffix= \
     --label-select-value connected_component \

kgtk filter \
     --input-file merged.tsv \
     --output-file filtered.tsv \
     --invert -p ';mw:SameAs;' \

kgtk compact \
    --input-file filtered.tsv \
    --output-file deduplicated.tsv \

     


kgtk connected_components \
     --properties mw:SameAs \
     --input-file kgtk/join/test/cc-file1.tsv \
     / lift \
     --input-file kgtk/join/test/cc-file1.tsv \
     --output-file - \
     --label-file - \
     --columns-to-lift node1 node2 \
     --lift-suffix= \
     --label-select-value connected_component \
     / filter \
     --input-file - \
     --output-file - \
     --invert -p ';mw:SameAs;' \
     / compact \
    --input-file - \
    --output-file connected.tsv

     


kgtk connected_components \
     --properties mw:SameAs \
     --input-file kgtk/join/test/cc-file1.tsv \
     / lift \
     --input-file kgtk/join/test/cc-file1.tsv \
     --label-file - \
     --columns-to-lift node1 node2 \
     --lift-suffix= \
     --label-select-value connected_component \
     / filter \
     --invert -p ';mw:SameAs;' \
     / compact \
    --output-file connected.tsv

     


kgtk connected_components --properties mw:SameAs \
     --input-file kgtk/join/test/cc-file1.tsv \
     / lift --columns-to-lift node1 node2 --lift-suffix= \
     --input-file kgtk/join/test/cc-file1.tsv \
     --label-file - \
     --label-select-value connected_component \
     / filter  --invert -p ';mw:SameAs;' \
     / compact --output-file connected.tsv

     



