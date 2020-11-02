#! /bin/bash

./import-split-wikidata-gzipped.sh
./sort-split-wikidata.sh

./process-edges.sh
./process-properties.sh

# ./deliver-to-kgtk-drive.sh
