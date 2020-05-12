#! /bin/sh
python3 kgtk/join/kgtkjoiner.py \
	kgtk/join/test/kgtkjoiner-test2-file1.tsv \
	kgtk/join/test/kgtkjoiner-test2-file2.tsv \
	--left-join \
	--output-file kgtk/join/test/kgtkjoiner-test2-left-output.tsv
