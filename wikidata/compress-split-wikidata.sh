#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

for TARGET in ${WIKIDATA_IMPORT_SPLIT_FILES[@]}
do
    echo -e "\nCompress the sorted ${TARGET} file."
    time ${GZIP_CMD} --keep --force --verbose \
	 ${DATADIR}/${TARGET}.tsv \
	|& tee ${LOGDIR}/${TARGET}-compress.log
done
