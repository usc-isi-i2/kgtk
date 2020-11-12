#! /bin/bash

source common.sh

kgtk $KGTK_FLAGS filter $VERBOSE --use-mgzip=$USE_MGZIP --regex\
     --input-file $DATADIR/claims.$SORTED_KGTK \
     -p '^P.*$ ;;' -o $DATADIR/claims.properties.$SORTED_KGTK

kgtk $KGTK_FLAGS filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file $DATADIR/qualifiers.$SORTED_KGTK \
    -p '^P.*$ ;;' -o $DATADIR/qualifiers.properties.$SORTED_KGTK

./count-properties.sh
./count-property-datatypes.sh


# ./split-properties-by-datatype.sh
# ./extract-qualifiers-for-property-datatype-splits.sh
