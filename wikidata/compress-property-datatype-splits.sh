#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Compress the property datatype splits.
for TARGET in ${WIKIDATATYPES[@]}
do
    TARGET_NAME=part.property.${TARGET}
    echo -e "\nCompress the sorted ${TARGET_NAME} file."
    time ${GZIP_CMD} --keep --force --verbose \
	 ${DATADIR}/${TARGET_NAME}.tsv \
	|& tee ${LOGDIR}/${TARGET_NAME}-compress.log
done
