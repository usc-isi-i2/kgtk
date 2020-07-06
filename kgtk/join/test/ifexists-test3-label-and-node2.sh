#! /bin/sh
python3 kgtk/join/ifexists.py --verbose \
	kgtk/join/test/ifexists-file6.tsv \
	--input-keys label node2 \
	--input-mode NONE \
	--filter-on kgtk/join/test/ifexists-file1.tsv \
	--filter-keys label node2 \
	--output-file kgtk/join/test/ifexists-test3-label-and-node2-output.tsv
