#! /bin/sh
python3 kgtk/join/simplejoiner.py \
	kgtk/join/test/simplejoiner-test1-file1.tsv \
	kgtk/join/test/simplejoiner-test1-file2.tsv \
	--left-join \
	--output-file kgtk/join/test/simplejoiner-test1-left-output.tsv
