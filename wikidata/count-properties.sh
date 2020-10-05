#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
echo -e "\nCount the properties in ${DATADIR}/${WIKIDATA_ALL_EDGES}-sorted.tsv."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL}-properties.tsv \
     --output-file ${DATADIR}${WIKIDATA_ALL}-property-counts.tsv \
     --column label \
     --label total-count \
     |& tee ${LOGDIR}/${WIKIDATA_ALL}-property-counts.log


# ==============================================================================
echo -e "\nLift the property labels:"
#
# CMR: This step takes 10 minutes on my home workstation because
# ${DATADIR}/${WIKIDATA_ALL}-labels-en-only-sorted.tsv is fairly large (6.6G
# as of 05-Oct-2020).
kgtk ${KGTK_FLAGS} \
     lift ${VERBOSE} \
     --input-file ${DATADIR}${WIKIDATA_ALL}-property-counts.tsv \
     --label-file ${DATADIR}/${WIKIDATA_ALL}-labels-en-only-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-property-counts-with-labels.tsv \
     --columns-to-lift node1 \
     --prefilter-labels \
     |& tee ${LOGDIR}/${WIKIDATA_ALL}-property-counts-with-labels.log

# ==============================================================================
echo -e "\nCompress the data product files."
time gzip --keep --force --verbose \
     ${DATADIR}/${WIKIDATA_ALL}-property-counts-with-labels.tsv \
    |& tee ${LOGDIR}/count-properties-compress.log

# ==============================================================================
echo -e "\nDeliver the compressed data products to the KGTK Google Drive."
time rsync --archive \
     ${DATADIR}/${WIKIDATA_ALL}-property-counts-with-labels.tsv.gz \
     ${PRODUCTDIR}/ \
    |& tee ${LOGDIR}/count-properties-deliver.log

     
     
