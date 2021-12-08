#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Count the property datatype distribution in the claims.
echo -e "\nCount unique datatypes in ${DATADIR}/claims.properties.tsv"
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} --use-mgzip ${USE_MGZIP} \
     --input-file ${DATADIR}/claims.properties.${SORTED_KGTK} \
     --column "node2;wikidatatype" \
     --output-file ${COUNTDIR}/claims.properties.datatypes.counts.${SORTED_KGTK} \
    | tee ${LOGDIR}/claims.properties.datatypes.counts.log
