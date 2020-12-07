#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
for TARGET in ${WIKIDATA_IMPORT_SPLIT_FILES[@]}
do
    echo -e "\nSort the ${TARGET} file."
    kgtk ${KGTK_FLAGS} \
	 sort2 ${VERBOSE} \
	 --input-file ${TEMPDIR}/${TARGET}.${UNSORTED_KGTK} \
	 --output-file ${DATADIR}/${TARGET}.${SORTED_KGTK} \
	 --gzip-command ${GZIP_CMD} \
	 --extra "${SORT_EXTRAS}" \
	|& tee ${LOGDIR}/${TARGET}-sorted.log
done
