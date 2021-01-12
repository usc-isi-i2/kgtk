#! /bin/bash

source common.sh

echo -e "\nExtract claims with a property in the node1 column."
kgtk $KGTK_FLAGS filter $VERBOSE --use-mgzip=$USE_MGZIP --regex\
     --input-file $DATADIR/claims.$SORTED_KGTK \
     -p '^P ;;' -o $DATADIR/claims.properties.$SORTED_KGTK

echo -e "\nExtract the qualifiers for claims with a property in node1."
kgtk $KGTK_FLAGS filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file $DATADIR/qualifiers.$SORTED_KGTK \
    -p '^P ;;' -o $DATADIR/qualifiers.properties.$SORTED_KGTK

