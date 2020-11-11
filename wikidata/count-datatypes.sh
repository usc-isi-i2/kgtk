#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Count the edge datatype distribution.
echo -e "\nCount unique datatypes in ${DATADIR}/all.tsv"
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} \
     --input-file ${DATADIR}/claims.${SORTED_KGTK} \
     --output-file ${DATADIR}/claims.datatypes.${SORTED_KGTK} \
     --column "node2;wikidatatype" \
     --use-mgzip ${USE_MGZIP} \
    |& tee ${LOGDIR}/claims.datatypes.log
