#! /bin/bash

./count-properties.sh
./count-property-datatypes.sh
./split-properties-by-datatype.sh
./compress-property-datatype-splits.sh
./deliver-property-datatype-splits.sh
./extract-qualifiers-for-property-datatype-splits.sh
./compress-qualifiers-for-property-datatype-splits.sh
./deliver-qualifiers-for-property-datatype-splits.sh
