#! /bin/sh
python3 kgtk/join/nodejoiner.py \
	kgtk/join/test/nodejoiner-test1-file1.tsv \
	kgtk/join/test/nodejoiner-test1-file2.tsv \
	--output-file kgtk/join/test/nodejoiner-test1-inner-output.tsv
