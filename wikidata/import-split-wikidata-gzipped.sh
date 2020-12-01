#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Setup working directories:
mkdir --verbose ${DATADIR}
mkdir --verbose ${LOGDIR}


# ==============================================================================
# Import the Wikidata dump file, getting labels, aliases, and descriptions
# in English and in all languages.
echo -e "\nImporting ${WIKIDATA_ALL_JSON} with labels, etc. in English and all languages"
kgtk ${KGTK_FLAGS} \
     import-wikidata \
     -i ${WIKIDATA_ALL_JSON} \
     --node-file ${TEMPDIR}/metadata.node.${UNSORTED_KGTK} \
     --minimal-edge-file ${TEMPDIR}/claims.raw.${UNSORTED_KGTK} \
     --minimal-qual-file ${TEMPDIR}/qualifiers.raw.${UNSORTED_KGTK} \
     --node-file-id-only \
     --explode-values False \
     --all-languages \
     --alias-edges True \
     --split-alias-file ${TEMPDIR}/aliases.${UNSORTED_KGTK} \
     --split-en-alias-file ${TEMPDIR}/aliases.en.${UNSORTED_KGTK} \
     --description-edges True \
     --split-description-file ${TEMPDIR}/descriptions.${UNSORTED_KGTK} \
     --split-en-description-file ${TEMPDIR}/descriptions.en.${UNSORTED_KGTK} \
     --label-edges True \
     --split-label-file ${TEMPDIR}/labels.${UNSORTED_KGTK} \
     --split-en-label-file ${TEMPDIR}/labels.en.${UNSORTED_KGTK} \
     --datatype-edges True \
     --split-datatype-file ${TEMPDIR}/metadata.property.datatypes.${UNSORTED_KGTK} \
     --entry-type-edges True \
     --split-type-file ${TEMPDIR}/metadata.types.${UNSORTED_KGTK} \
     --sitelink-edges True \
     --sitelink-verbose-edges True \
     --split-sitelink-file ${TEMPDIR}/sitelinks.raw.${UNSORTED_KGTK} \
     --split-en-sitelink-file ${TEMPDIR}/sitelinks.en.raw.${UNSORTED_KGTK} \
     --value-hash-width 6 \
     --claim-id-hash-width 8 \
     --use-kgtkwriter True \
     --use-mgzip-for-input True \
     --use-mgzip-for-output True \
     --use-shm True \
     --procs 12 \
     --mapper-batch-size 5 \
     --max-size-per-mapper-queue 3 \
     --single-mapper-queue True \
     --collect-results True \
     --collect-seperately True\
     --collector-batch-size 10 \
     --collector-queue-per-proc-size 3 \
     --progress-interval 500000 \
    |& tee ${LOGDIR}/import-split-wikidata.log
