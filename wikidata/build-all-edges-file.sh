#! /bin/bash

source common.sh

kgtk ${KGTK_FLAGS} \
     cat ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --input-file ${TEMPDIR}/claims.${UNSORTED_KGTK} \
     --input-file ${TEMPDIR}/qualifiers.${UNSORTED_KGTK} \
     --input-file ${TEMPDIR}/aliases.${UNSORTED_KGTK} \
     --input-file ${TEMPDIR}/descriptions.${UNSORTED_KGTK} \
     --input-file ${TEMPDIR}/labels.${UNSORTED_KGTK} \
     --input-file ${TEMPDIR}/sitelinks.${UNSORTED_KGTK} \
     --input-file ${TEMPDIR}/sitelinks.qualifiers.${UNSORTED_KGTK} \
     --input-file ${TEMPDIR}/metadata.types.${UNSORTED_KGTK} \
     --input-file ${TEMPDIR}/metadata.property.datatypes.${UNSORTED_KGTK} \
/ sort2 ${VERBOSE} \
     --gzip-command ${GZIP_CMD} \
     --extra "${SORT_EXTRAS}" \
     --output-file ${DATADIR}/all.${SORTED_KGTK}

