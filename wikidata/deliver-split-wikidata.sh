#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
for TARGET in ${WIKIDATA_IMPORT_SPLIT_FILES[@]}
do
    echo -e "\nDeliver the compressed ${TARGET} file to the KGTK Google Drive."
    time rsync --archive --verbose \
	 ${DATADIR}/${TARGET}.${SORTED_KGTK} \
	 ${PRODUCTDIR}/ \
	|& tee ${LOGDIR}/${TARGET}-deliver.log
done
