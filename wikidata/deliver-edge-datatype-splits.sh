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
# Compress and deliver the edge datatypes splits.
for TARGET in ${WIKIDATATYPES[@]}
do
    TARGET_NAME=part.${TARGET}
    echo -e "\nCompress the sorted ${TARGET} file."
    time gzip --keep --force --verbose \
	 ${DATADIR}/${TARGET_NAME}.tsv \
	|& tee ${LOGDIR}/${TARGET_NAME}-compress.log

    echo -e "\nDeliver the compressed ${TARGET_NAME} file to the KGTK Google Drive."
    time rsync --archive --verbose \
	 ${DATADIR}/${TARGET_NAME}.tsv.gz \
	 ${PRODUCTDIR}/ \
	|& tee ${LOGDIR}/${TARGET_NAME}-deliver.log

    echo -e "\nCompress the sorted qualifiers for the ${TARGET} properties."
    time gzip --keep --force --verbose \
	 ${DATADIR}/${TARGET_NAME}.qual.tsv \
	|& tee ${LOGDIR}/${TARGET_NAME}.qual-compress.log

    echo -e "\nDeliver the compressed qualifiers for ${TARGET_NAME} file to the KGTK Google Drive."
    time rsync --archive --verbose \
	 ${DATADIR}/${TARGET_NAME}.qual.tsv.gz \
	 ${PRODUCTDIR}/ \
	|& tee ${LOGDIR}/${TARGET_NAME}.qual-deliver.log
done
