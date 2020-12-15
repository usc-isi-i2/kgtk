#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
echo -e "\nSort the sitelinks file."
kgtk ${KGTK_FLAGS} \
     sort2 ${VERBOSE} --gzip-command=${GZIP_CMD} \
     --input-file ${DATADIR}/sitelinks.${UNSORTED_KGTK} \
     --output-file ${DATADIR}/sitelinks.${SORTED_KGTK} \
     --extra "${SORT_EXTRAS}"

echo -e "\nSort the sitelinks.qualifiers file."
kgtk ${KGTK_FLAGS} \
     sort2 ${VERBOSE} --gzip-command=${GZIP_CMD} \
     --input-file ${DATADIR}/sitelinks.qualifiers.${UNSORTED_KGTK} \
     --output-file ${DATADIR}/sitelinks.qualifiers.${SORTED_KGTK} \
     --extra "${SORT_EXTRAS}"

echo -e "\nSort the sitelinks.en file."
kgtk ${KGTK_FLAGS} \
     sort2 ${VERBOSE} --gzip-command=${GZIP_CMD} \
     --input-file ${DATADIR}/sitelinks.en.${UNSORTED_KGTK} \
     --output-file ${DATADIR}/sitelinks.en.${SORTED_KGTK} \
     --extra "${SORT_EXTRAS}"

echo -e "\nSort the sitelinks.en.qualifiers file."
kgtk ${KGTK_FLAGS} \
     sort2 ${VERBOSE} --gzip-command=${GZIP_CMD} \
     --input-file ${DATADIR}/sitelinks.en.qualifiers.${UNSORTED_KGTK} \
     --output-file ${DATADIR}/sitelinks.en.qualifiers.${SORTED_KGTK} \
     --extra "${SORT_EXTRAS}"
