#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Setup working directories:
mkdir --verbose ${DATADIR}
mkdir --verbose ${LOGDIR}

# ==============================================================================
# Extract the qualifiers for the edge datatypes splits.
for TARGET in ${WIKIDATATYPES[@]}
do
    TARGET_NAME=part.${TARGET}

    echo -e "\nExtract any qualifiers for the properties in ${TARGET_NAME}."
    kgtk ${KGTK_FLAGS} \
	 ifexists ${VERBOSE} \
	 --input-file ${DATADIR}/qual.tsv \
	 --filter-on ${DATADIR}/${TARGET_NAME}.tsv \
	 --output-file ${DATADIR}/${TARGET_NAME}.qual.tsv \
	 --input-keys node1 \
	 --filter-keys id \
	|& tee ${LOGDIR}/${TARGET_NAME}.qual.log
done
