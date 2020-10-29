#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Deliver the qualifiers for the edge datatypes splits.
for TARGET in ${WIKIDATATYPES[@]}
do
    TARGET_NAME=part.${TARGET}

    echo -e "\nDeliver the compressed qualifiers for ${TARGET_NAME} file to the KGTK Google Drive."
    time rsync --archive --verbose \
	 ${DATADIR}/${TARGET_NAME}.qual.tsv.gz \
	 ${PRODUCTDIR}/ \
	|& tee ${LOGDIR}/${TARGET_NAME}.qual-deliver.log
done
