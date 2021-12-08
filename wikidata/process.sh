#! /bin/bash

./import-split-wikidata-gzipped-clean.sh
./split-missing-values.sh
./split-sitelink-qualifiers.sh
./sort-split-wikidata.sh
./build-all-edges-file.sh
./check-for-unclaimed-qualifiers.sh

./process-edges.sh
./process-properties.sh

# Compute various counts and consistency checks.
./process-counts.sh

# ./deliver-to-kgtk-drive.sh
