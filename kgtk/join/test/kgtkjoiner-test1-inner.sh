#! /bin/sh
python3 kgtk/join/kgtkjoiner.py \
	kgtk/join/test/kgtkjoiner-test1-file1.tsv \
	kgtk/join/test/kgtkjoiner-test1-file2.tsv \
	--output-file kgtk/join/test/kgtkjoiner-test1-inner-output.tsv
