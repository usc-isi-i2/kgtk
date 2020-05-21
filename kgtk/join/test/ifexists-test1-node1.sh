#! /bin/sh
python3 kgtk/join/ifexists.py \
	kgtk/join/test/ifexists-test1-file1.tsv \
	--input-keys node1 \
	--filter-on kgtk/join/test/ifexists-test1-file2.tsv \
	--filter-keys node1 \
	--output-file kgtk/join/test/ifexists-test1-node1-output.tsv
