#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Deliver the edge datatype distribution.
echo -e "\nDeliver the all.datatypes file to the KGTK Google Drive."
time rsync --archive --verbose \
     ${DATADIR}/all.datatypes.${SORTED_KGTK} \
     ${PRODUCTDIR}/ \
    |& tee ${LOGDIR}/all.datatypes-deliver.log
    
