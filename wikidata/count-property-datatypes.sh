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
     --input-file ${DATADIR}/part.property.tsv \
     --output-file ${DATADIR}/part.property.datatypes.tsv \
     --column "node2;wikidatatype" \
    |& tee ${LOGDIR}/part.property.datatypes.log

# ==============================================================================
# Deliver the property datatype distribution.  It is small, so don't bother
# compressing it.
echo -e "\nDeliver the part.property.datatypes file to the KGTK Google Drive."
time rsync --archive --verbose \
     ${DATADIR}/part.property.datatypes.tsv \
     ${PRODUCTDIR}/ \
    |& tee ${LOGDIR}/part.property.datatypes-deliver.log
