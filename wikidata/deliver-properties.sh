#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
echo -e "\nDeliver the compressed data products to the KGTK Google Drive."
time rsync --archive --verbose \
     ${DATADIR}/part.property.counts-with-labels.${SORTED_KGTK} \
     ${PRODUCTDIR}/ \
    |& tee ${LOGDIR}/part.property.counts-with-labels-deliver.log

     
     
