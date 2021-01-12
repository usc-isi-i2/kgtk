#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Deliver the property datatype distribution.  It is small, so don't bother
# compressing it.
echo -e "\nDeliver the part.property.datatypes file to the KGTK Google Drive."
time rsync --archive --verbose \
     ${DATADIR}/part.property.datatypes.${SORTED_KGTK} \
     ${PRODUCTDIR}/ \
    |& tee ${LOGDIR}/part.property.datatypes-deliver.log
