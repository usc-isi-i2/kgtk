#! /bin/sh
python3 kgtk/join/simplejoiner.py \
	kgtk/join/test/simplejoiner-test1-file1.tsv \
	kgtk/join/test/simplejoiner-test1-file2.tsv \
	--output-file kgtk/join/test/simplejoiner-test1-inner-output.tsv
