#! /bin/sh
python3 kgtk/join/ifexists.py \
	kgtk/join/test/ifexists-test1-file1.tsv \
	kgtk/join/test/ifexists-test1-file2.tsv \
	--left-keys node1 \
	--right-keys node1 \
	--output-file kgtk/join/test/ifexists-test1-node1-output.tsv
