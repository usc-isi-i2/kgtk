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
# Count the edge datatype distribution.
echo -e "\nCount unique datatypes in ${DATADIR}/all.tsv"
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} \
     --input-file ${DATADIR}/all.tsv \
     --output-file ${DATADIR}/all.datatypes.tsv \
     --column "node2;wikidatatype" \
    |& tee ${LOGDIR}/all.datatypes.log

# ==============================================================================
# Deliver the edge datatype distribution.  It is small, so don't bother
# compressing it.
echo -e "\nDeliver the all.datatypes file to the KGTK Google Drive."
time rsync --archive --verbose \
     ${DATADIR}/all.datatypes.tsv \
     ${PRODUCTDIR}/ \
    |& tee ${LOGDIR}/all.datatypes-deliver.log
    
