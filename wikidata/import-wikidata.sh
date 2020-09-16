#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source scripts/common.sh

# ==============================================================================
# Setup working directories:
mkdir --verbose ${DATADIR}
mkdir --verbose ${LOGDIR}


# ==============================================================================
# Import the Wikidata dump file, getting labels, aliases, and descriptions
# in all languages.
#
# Note: I use 8 processors on my home system.
echo -e "\nImporting ${WIKIDATA_ALL_JSON} with labels, etc. in all languages"
kgtk ${KGTK_FLAGS} \
     import-wikidata ${VERBOSE} \
     -i ${WIKIDATA_ALL_JSON} \
     --node ${WIKIDATA_ALL_NODES}-all-lang.tsv \
     --edge ${WIKIDATA_ALL_EDGES}.tsv \
     --qual ${WIKIDATA_ALL_QUALIFIERS}.tsv \
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

# Repeat the import, getting only the English aliases, descriptors, and labels.
# As of 15-Sep-2020, this is faster than filtering after extraction.
echo -e "\nImporting ${WIKIDATA_ALL_JSON} with labels, etc. in all languages"
kgtk ${KGTK_FLAGS} \
     import-wikidata ${VERBOSE} \
     -i ${WIKIDATA_ALL_JSON} \
     --node ${WIKIDATA_ALL_NODES}-en-only.tsv \
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

# Repeat the import, getting English, Spanish, Russian, and Ukranian subset of
# the aliases, descriptions, and labels,
echo -e "\nImporting ${WIKIDATA_ALL_JSON} with labels, etc. in English, Spanish, Russian, and Ukranian"
kgtk ${KGTK_FLAGS} \
     import-wikidata ${VERBOSE} \
     -i ${WIKIDATA_ALL_JSON} \
     --node ${WIKIDATA_ALL_NODES}-en-es-ru-uk.tsv \
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

echo -e "\nCompress the files we have imported."
time gzip --keep --force --verbose \
     ${WIKIDATA_ALL_NODES}-all-lang.tsv \
     ${WIKIDATA_ALL_EDGES}.tsv \
     ${WIKIDATA_ALL_QUALIFIERS}.tsv \
     ${WIKIDATA_ALL_NODES}-en-only.tsv \
     ${WIKIDATA_ALL_NODES}-en-es-ru-uk.tsv \
    |& tee ${LOGDIR}/import-wikidata-compress.log

echo -e "\nDeliver the compressed extracted data to the KGTK Google Drive."
time rsync --archive \
     ${WIKIDATA_ALL_NODES}-all-lang.tsv \
     ${WIKIDATA_ALL_EDGES}.tsv \
     ${WIKIDATA_ALL_QUALIFIERS}.tsv \
     ${WIKIDATA_ALL_NODES}-en-only.tsv \
     ${WIKIDATA_ALL_NODES}-en-es-ru-uk.tsv \
     ${PRODUCTDIR}/ \
    |& tee ${LOGDIR}/import-wikidata-deliver.log

     
     
