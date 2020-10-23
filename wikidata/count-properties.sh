#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
echo -e "\nCount the properties in ${DATADIR}/${WIKIDATA_ALL_EDGES}.tsv."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} \
     --input-file ${DATADIR}/part.property.tsv \
     --output-file ${DATADIR}/part.property.counts.tsv \
     --column label \
     --label total-count \
     |& tee ${LOGDIR}/part.property.counts.log


# ==============================================================================
echo -e "\nLift the property labels:"
#
# CMR: This step takes 10 minutes on my home workstation because
# ${DATADIR}/${WIKIDATA_ALL}-labels-en-only-sorted.tsv is fairly large (6.6G
# as of 05-Oct-2020).
kgtk ${KGTK_FLAGS} \
     lift ${VERBOSE} \
     --input-file ${DATADIR}/part.property.counts.tsv \
     --label-file ${DATADIR}/part.label.en.tsv \
     --output-file ${DATADIR}/part.property.counts-with-labels.tsv \
     --columns-to-lift node1 \
     --prefilter-labels \
     |& tee ${LOGDIR}/part.property.counts-with-labels.log

# ==============================================================================
echo -e "\nCompress the data product files."
time gzip --keep --force --verbose \
     ${DATADIR}/part.property.counts-with-labels.tsv \
    |& tee ${LOGDIR}/part.property.counts-with-labels-compress.log

# ==============================================================================
echo -e "\nDeliver the compressed data products to the KGTK Google Drive."
time rsync --archive --verbose \
     ${DATADIR}/part.property.counts-with-labels.tsv.gz \
     ${PRODUCTDIR}/ \
    |& tee ${LOGDIR}/part.property.counts-with-labels-deliver.log

     
     
