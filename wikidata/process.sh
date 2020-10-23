#! /bin/bash

./import-split-wikidata.sh
./count-properties.sh
./count-datatypes.sh
./count-property-datatypes.sh
./split-edges-by-datatype.sh
./extract-qualifiers-for-edge-datatype-splits.sh
./deliver-edge-datatype-splits.sh
./split-properties-by-datatype.sh
./extract-qualifiers-for-property-datatype-splits.sh
./deliver-property-datatype-splits.sh
