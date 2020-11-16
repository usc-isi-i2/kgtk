#! /bin/bash

source common.sh

kgtk ${KGTK_FLAGS} \
     cat ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --input-file ${DATADIR}/claims.${UNSORTED_KGTK} \
     --input-file ${DATADIR}/qualifiers.${UNSORTED_KGTK} \
     --input-file ${DATADIR}/aliases.${UNSORTED_KGTK} \
     --input-file ${DATADIR}/descriptions.${UNSORTED_KGTK} \
     --input-file ${DATADIR}/labels.${UNSORTED_KGTK} \
     --input-file ${DATADIR}/sitelinks.${UNSORTED_KGTK} \
     --input-file ${DATADIR}/metadata.types.${UNSORTED_KGTK} \
     --input-file ${DATADIR}/metadata.property.datatypes.${UNSORTED_KGTK} \
/ sort2 ${VERBOSE} \
     --output-file ${DATADIR}/all.${SORTED_KGTK} \
     --gzip-command ${GZIP_CMD} \
     --extra "${SORT_EXTRAS}" \


