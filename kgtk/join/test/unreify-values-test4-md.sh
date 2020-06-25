#! /bin/bash

python3 kgtk/unreify/kgtkunreifyvalues.py \
	-i kgtk/join/test/unreify-values-file3.tsv \
	--trigger-label rdf:type \
	--trigger-node2 ont:Confidence \
	--value-label ont:confidenceValue \
	--old-label ont:confidence \
	--output-format=md \
	--allow-multiple-values \
	
