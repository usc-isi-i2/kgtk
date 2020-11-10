#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Count the property datatype distribution.
echo -e "\nCount unique datatypes in ${DATADIR}/part.property.tsv"
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} \
     --input-file ${DATADIR}/part.property.${SORTED_KGTK} \
     --output-file ${DATADIR}/part.property.datatypes.${SORTED_KGTK} \
     --column "node2;wikidatatype" \
     --use-mgzip ${USE_MGZIP} \
    |& tee ${LOGDIR}/part.property.datatypes.log
