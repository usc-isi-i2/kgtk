#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Compress the qualifiers for the edge datatypes splits.
for TARGET in ${WIKIDATATYPES[@]}
do
    TARGET_NAME=part.${TARGET}
    echo -e "\nCompress the sorted qualifiers for the ${TARGET} edges."
    time ${GZIP_CMD} --keep --force --verbose \
	 ${DATADIR}/${TARGET_NAME}.qual.tsv \
	|& tee ${LOGDIR}/${TARGET_NAME}.qual-compress.log
done
