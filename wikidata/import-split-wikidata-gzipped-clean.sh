#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Setup working directories:
#mkdir --verbose ${DATADIR}
mkdir -p ${DATADIR}
#mkdir --verbose ${TEMPDIR}
mkdir -p ${TEMPDIR}
#mkdir --verbose ${LOGDIR}
mkdir -p ${LOGDIR}
#mkdir --verbose ${COUNTDIR}
mkdir -p ${COUNTDIR}


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
     --invalid-edge-file ${TEMPDIR}/claims.badvalue.${UNSORTED_KGTK} \
     --invalid-qual-file ${TEMPDIR}/qualifiers.badvalue.${UNSORTED_KGTK} \
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
     --reference-edges True \
     --reference-detail-edges True \
     --split-reference-file ${TEMPDIR}/references.raw.${UNSORTED_KGTK} \
     --sitelink-edges True \
     --sitelink-verbose-edges True \
     --split-sitelink-file ${TEMPDIR}/sitelinks.raw.${UNSORTED_KGTK} \
     --split-en-sitelink-file ${TEMPDIR}/sitelinks.en.raw.${UNSORTED_KGTK} \
     --value-hash-width 6 \
     --claim-id-hash-width 8 \
     --use-mgzip-for-input False \
     --use-mgzip-for-output False \
     --use-shm True \
     --procs 6 \
     --mapper-batch-size 5 \
     --max-size-per-mapper-queue 3 \
     --single-mapper-queue True \
     --collect-seperately True\
     --collector-batch-size 5 \
     --collector-queue-per-proc-size 3 \
     --progress-interval 500000 \
     --clean \
     --allow-end-of-day False \
     --repair-month-or-day-zero \
     --minimum-valid-year 1 \
     --maximum-valid-year 9999 \
     --validate-fromisoformat \
     --repair-lax-coordinates \
     --allow-language-suffixes \
     --allow-wikidata-lq-strings \
    | tee ${LOGDIR}/import-split-wikidata.log


#     --additional-language-codes cnr hyw syz bh mo eml simple \
#     --ignore-minimum-year \
#     --ignore-maximum-year \
#     --allow-out-of-range-coordinates \
