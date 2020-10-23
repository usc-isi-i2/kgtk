#! /bin/bash

./count-datatypes.sh
./split-edges-by-datatype.sh
./compress-edge-datatype-splits.sh
./deliver-edge-datatype-splits.sh
./extract-qualifiers-for-edge-datatype-splits.sh
./compress-qualifiers-for-edge-datatype-splits.sh
./deliver-qualifiers-for-edge-datatype-splits.sh
