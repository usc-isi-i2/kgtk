#! /bin/bash

# This script is temporary until `kgtk import-wikidata` performs the split on its own.
source common.sh

# ==============================================================================
# Split the sitelink qualifiers.
echo -e "\nSplit ${DATADIR}/sitelinksraw.${SORTED_KGTK}"
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --input-file ${DATADIR}/sitelinksraw.${UNSORTED_KGTK} \
     --pattern "; sitelink-badge,sitelink-language,sitelink-site,sitelink-title ;" \
     --output-file ${DATADIR}/sitelinks.qualifiers.${UNSORTED_KGTK} \
     --reject-file ${DATADIR}/sitelinks.${UNSORTED_KGTK} \
    |& tee ${LOGDIR}/split-sitelink-qualifiers.log

echo -e "\nSplit ${DATADIR}/sitelinksraw.en.${SORTED_KGTK}"
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --input-file ${DATADIR}/sitelinksraw.en.${UNSORTED_KGTK} \
     --pattern "; sitelink-badge,sitelink-language,sitelink-site,sitelink-title ;" \
     --output-file ${DATADIR}/sitelinks.en.qualifiers.${UNSORTED_KGTK} \
     --reject-file ${DATADIR}/sitelinks.en.${UNSORTED_KGTK} \
    |& tee ${LOGDIR}/split-sitelink-en-qualifiers.log
