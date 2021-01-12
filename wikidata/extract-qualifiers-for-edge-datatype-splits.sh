#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Extract the qualifiers for the edge datatypes splits.
for TARGET in ${WIKIDATATYPES[@]}
do
    echo -e "\nExtract any qualifiers for the properties in claims.${TARGET}."
    kgtk ${KGTK_FLAGS} \
	 ifexists ${VERBOSE} \
	 --input-file ${DATADIR}/qualifiers.${SORTED_KGTK} \
	 --filter-on ${DATADIR}/claims.${TARGET}.${SORTED_KGTK} \
	 --output-file ${DATADIR}/qualifiers.${TARGET}.${SORTED_KGTK} \
	 --input-keys node1 \
	 --filter-keys id \
	 --presorted \
	 --use-mgzip ${USE_MGZIP} \
	|& tee ${LOGDIR}/qualifiers.${TARGET}.log
done
