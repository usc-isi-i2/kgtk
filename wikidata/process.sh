#! /bin/bash

./import-split-wikidata.sh
./process-split-wikidata.sh
./process-edges.sh
./process-properties.sh
