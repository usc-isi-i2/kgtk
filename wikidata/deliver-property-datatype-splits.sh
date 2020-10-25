#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Deliver the property datatype splits.
for TARGET in ${WIKIDATATYPES[@]}
do
    TARGET_NAME=part.property.${TARGET}
    echo -e "\nDeliver the compressed ${TARGET_NAME} file to the KGTK Google Drive."
    time rsync --archive --verbose \
	 ${DATADIR}/${TARGET_NAME}.tsv.gz \
	 ${PRODUCTDIR}/ \
	|& tee ${LOGDIR}/${TARGET_NAME}-deliver.log
done
