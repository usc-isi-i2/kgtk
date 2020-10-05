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
# in all languages.
echo -e "\nImporting ${WIKIDATA_ALL_JSON} with labels, etc. in all languages"
kgtk ${KGTK_FLAGS} \
     import-wikidata \
     -i ${WIKIDATA_ALL_JSON} \
     --node ${DATADIR}/${WIKIDATA_ALL_NODES}-all-lang.tsv \
     --edge ${DATADIR}/${WIKIDATA_ALL_EDGES}.tsv \
     --qual ${DATADIR}/${WIKIDATA_ALL_QUALIFIERS}.tsv \
     --explode-values False \
     --all-languages \
     --alias-edges False \
     --description-edges False \
     --label-edges False \
     --use-kgtkwriter True \
     --use-shm True \
     --procs 4 \
     --mapper-batch-size 5 \
     --max-size-per-mapper-queue 10 \
     --single-mapper-queue True \
     --collect-results True \
     --collect-seperately True\
     --collector-batch-size 10 \
     --collector-queue-per-proc-size 20 \
     --progress-interval 500000 \
    |& tee ${LOGDIR}/import-wikidata.log

# ==============================================================================
# Repeat the import, getting only the English aliases, descriptors, and labels.
# As of 15-Sep-2020, this is faster than filtering after extraction.
echo -e "\nImporting ${WIKIDATA_ALL_JSON} with labels, etc. in English"
kgtk ${KGTK_FLAGS} \
     import-wikidata \
     -i ${WIKIDATA_ALL_JSON} \
     --node ${DATADIR}/${WIKIDATA_ALL_NODES}-en-only.tsv \
     --explode-values False \
     --lang en \
     --use-kgtkwriter True \
     --use-shm True \
     --procs 6 \
     --mapper-batch-size 5 \
     --max-size-per-mapper-queue 10 \
     --single-mapper-queue True \
     --collect-results True \
     --collect-seperately True\
     --collector-batch-size 10 \
     --collector-queue-per-proc-size 20 \
     --progress-interval 500000 \
    |& tee ${LOGDIR}/import-wikidata-en-only.log

# ==============================================================================
# Repeat the import, getting English, Spanish, Russian, and Ukranian subset of
# the aliases, descriptions, and labels,
echo -e "\nImporting ${WIKIDATA_ALL_JSON} with labels, etc. in English, Spanish, Russian, and Ukranian"
kgtk ${KGTK_FLAGS} \
     import-wikidata \
     -i ${WIKIDATA_ALL_JSON} \
     --node ${DATADIR}/${WIKIDATA_ALL_NODES}-en-es-ru-uk.tsv \
     --explode-values False \
     --lang en,es,ru,uk \
     --use-kgtkwriter True \
     --use-shm True \
     --procs 6 \
     --mapper-batch-size 5 \
     --max-size-per-mapper-queue 10 \
     --single-mapper-queue True \
     --collect-results True \
     --collect-seperately True\
     --collector-batch-size 10 \
     --collector-queue-per-proc-size 20 \
     --progress-interval 500000 \
    |& tee ${LOGDIR}/import-wikidata-en-es-ru-uk.log

# ==============================================================================
echo -e "\nSort the files we have imported."
kgtk ${KGTK_FLAGS} \
     sort2 ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL_NODES}-all-lang.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL_NODES}-all-lang-sorted.tsv \
     --extra "${SORT_EXTRAS}" \
    |& tee ${LOGDIR}/${WIKIDATA_ALL_NODES}-all-lang-sorted.log

kgtk ${KGTK_FLAGS} \
     sort2 ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL_EDGES}.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL_EDGES}-sorted.tsv \
     --extra "${SORT_EXTRAS}" \
    |& tee ${LOGDIR}/${WIKIDATA_ALL_EDGES}-sorted.log

kgtk ${KGTK_FLAGS} \
     sort2 ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL_QUALIFIERS}.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL_QUALIFIERS}-sorted.tsv \
     --extra "${SORT_EXTRAS}" \
    |& tee ${LOGDIR}/${WIKIDATA_ALL_QUALIFIERS}-sorted.log

kgtk ${KGTK_FLAGS} \
     sort2 ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL_NODES}-en-only.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL_NODES}-en-only-sorted.tsv \
     --extra "${SORT_EXTRAS}" \
    |& tee ${LOGDIR}/${WIKIDATA_ALL_NODES}-en-only-sorted.log

kgtk ${KGTK_FLAGS} \
     sort2 ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL_NODES}-en-es-ru-uk.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL_NODES}-en-es-ru-uk-sorted.tsv \
     --extra "${SORT_EXTRAS}" \
    |& tee ${LOGDIR}/${WIKIDATA_ALL_NODES}-en-es-ru-uk-sorted.log

# ==============================================================================
echo -e "\nCompress the sorted files to create the product files."
time gzip --keep --force --verbose \
     ${DATADIR}/${WIKIDATA_ALL_NODES}-all-lang-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL_EDGES}-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL_QUALIFIERS}-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL_NODES}-en-only-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL_NODES}-en-es-ru-uk-sorted.tsv \
    |& tee ${LOGDIR}/import-wikidata-compress.log

# ==============================================================================
echo -e "\nDeliver the compressed data products to the KGTK Google Drive."
time rsync --archive --verbose \
     ${DATADIR}/${WIKIDATA_ALL_NODES}-all-lang-sorted.tsv.gz \
     ${DATADIR}/${WIKIDATA_ALL_EDGES}-sorted.tsv.gz \
     ${DATADIR}/${WIKIDATA_ALL_QUALIFIERS}-sorted.tsv.gz \
     ${DATADIR}/${WIKIDATA_ALL_NODES}-en-only-sorted.tsv.gz \
     ${DATADIR}/${WIKIDATA_ALL_NODES}-en-es-ru-uk-sorted.tsv.gz \
     ${PRODUCTDIR}/ \
    |& tee ${LOGDIR}/import-wikidata-deliver.log

     
     
