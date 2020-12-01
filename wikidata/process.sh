#! /bin/bash

./import-split-wikidata-gzipped.sh
./split-missing-values.sh
./split-sitelink-qualifiers.sh
./sort-split-wikidata.sh
./build-all-edges-file.sh
./check-for-unclaimed-qualifiers.sh

./process-edges.sh
./process-properties.sh

./process-counts.sh

# ./deliver-to-kgtk-drive.sh
