#! /bin/bash

python3 kgtk/unreify/kgtkunreifyvalues.py -v \
	-i kgtk/join/test/unreify-values-file1.tsv \
	--trigger-label rdf:type \
	--trigger-node2 ont:Confidence \
	--value-label ont:confidenceValue \
	--old-label ont:confidence \
