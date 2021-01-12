#! /bin/bash

# This script is temporary until `kgtk import-wikidata` performs the split on its own.
source common.sh

# ==============================================================================
# Split the sitelink qualifiers.
echo -e "\nSplit ${TEMPDIR}/sitelinksraw.${SORTED_KGTK}"
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --input-file ${TEMPDIR}/sitelinks.raw.${UNSORTED_KGTK} \
     --pattern "; sitelink-badge,sitelink-language,sitelink-site,sitelink-title ;" \
     --output-file ${TEMPDIR}/sitelinks.qualifiers.${UNSORTED_KGTK} \
     --reject-file ${TEMPDIR}/sitelinks.${UNSORTED_KGTK} \
    |& tee ${LOGDIR}/split-sitelink-qualifiers.log

echo -e "\nSplit ${TEMPDIR}/sitelinksraw.en.${SORTED_KGTK}"
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --input-file ${TEMPDIR}/sitelinks.en.raw.${UNSORTED_KGTK} \
     --pattern "; sitelink-badge,sitelink-language,sitelink-site,sitelink-title ;" \
     --output-file ${TEMPDIR}/sitelinks.en.qualifiers.${UNSORTED_KGTK} \
     --reject-file ${TEMPDIR}/sitelinks.en.${UNSORTED_KGTK} \
    |& tee ${LOGDIR}/split-sitelink-en-qualifiers.log
