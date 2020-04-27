#! /bin/sh
python3 kgtk/join/edgejoiner.py \
	kgtk/join/test/edgejoiner-test1-file1.tsv \
	kgtk/join/test/edgejoiner-test1-file2.tsv \
	--output-file kgtk/join/test/edgejoiner-test1-inner-output.tsv
