#! /bin/sh
python3 kgtk/join/edgejoiner.py \
	kgtk/join/test/edgejoiner-test1-file1.tsv \
	kgtk/join/test/edgejoiner-test1-file2.tsv \
	--left-join \
	--output-file kgtk/join/test/edgejoiner-test1-left-output.tsv
