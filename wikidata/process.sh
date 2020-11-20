#! /bin/bash

./import-split-wikidata-gzipped.sh
./split-sitelink-qualifiers.sh
./sort-split-wikidata.sh
./build-all-edges-file.sh

./process-edges.sh
./process-properties.sh

# ./deliver-to-kgtk-drive.sh
