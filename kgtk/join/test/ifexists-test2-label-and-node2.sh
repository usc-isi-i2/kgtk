#! /bin/sh
python3 kgtk/join/ifexists.py \
	kgtk/join/test/ifexists-test2-file1.tsv \
	--input-keys label node2 \
	--filter-on kgtk/join/test/ifexists-test2-file2.tsv \
	--filter-keys label node2 \
	--filter-mode NONE \
	--output-file kgtk/join/test/ifexists-test2-label-and-node2-output.tsv
