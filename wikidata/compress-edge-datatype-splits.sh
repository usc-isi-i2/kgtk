#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Compress the edge datatypes splits.
for TARGET in ${WIKIDATATYPES[@]}
do
    TARGET_NAME=part.${TARGET}
    echo -e "\nCompress the sorted ${TARGET} file."
    time ${GZIP_CMD} --keep --force --verbose \
	 ${DATADIR}/${TARGET_NAME}.tsv \
	|& tee ${LOGDIR}/${TARGET_NAME}-compress.log
done
