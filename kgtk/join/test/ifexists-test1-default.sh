#! /bin/sh
python3 kgtk/join/ifexists.py \
	kgtk/join/test/ifexists-test1-file1.tsv \
	--filter-on kgtk/join/test/ifexists-test1-file2.tsv \
	--output-file kgtk/join/test/ifexists-test1-default-output.tsv
