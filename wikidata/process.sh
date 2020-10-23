#! /bin/bash

./import-split-wikidata.sh
./count-properties.sh
./count-datatypes.sh
./count-property-datatypes.sh
./split-properties-by-datatype-for-pedro.sh
