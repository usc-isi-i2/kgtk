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
# in Englisn and in all languages.
echo -e "\nImporting ${WIKIDATA_ALL_JSON} with labels, etc. in English and all languages"
kgtk ${KGTK_FLAGS} \
     import-wikidata \
     -i ${WIKIDATA_ALL_JSON} \
     --node-file ${DATADIR}/${WIKIDATA_ALL_NODES}.tsv \
     --detailed-edge-file ${DATADIR}/${WIKIDATA_ALL_EDGES}-full.tsv \
     --minimal-edge-file ${DATADIR}/${WIKIDATA_ALL_EDGES}.tsv \
     --detailed-qual-file ${DATADIR}/${WIKIDATA_ALL_QUALIFIERS}-full.tsv \
     --minimal-qual-file ${DATADIR}/${WIKIDATA_ALL_QUALIFIERS}.tsv \
     --node-file-id-only \
     --explode-values False \
     --all-languages \
     --alias-edges True \
     --split-alias-file ${DATADIR}/${WIKIDATA_ALL}-aliases-all-lang.tsv \
     --split-en-alias-file ${DATADIR}/${WIKIDATA_ALL}-aliases-en-only.tsv \
     --description-edges True \
     --split-description-file ${DATADIR}/${WIKIDATA_ALL}-descriptions-all-lang.tsv \
     --split-en-description-file ${DATADIR}/${WIKIDATA_ALL}-descriptions-en-only.tsv \
     --label-edges True \
     --split-label-file ${DATADIR}/${WIKIDATA_ALL}-labels-all-lang.tsv \
     --split-en-label-file ${DATADIR}/${WIKIDATA_ALL}-labels-en-only.tsv \
     --datatype-edges True \
     --split-datatype-file ${DATADIR}/${WIKIDATA_ALL}-datatypes.tsv \
     --entry-type-edges True \
     --split-type-file ${DATADIR}/${WIKIDATA_ALL}-types.tsv \
     --sitelink-edges True \
     --sitelink-verbose-edges True \
     --split-sitelink-file ${DATADIR}/${WIKIDATA_ALL}-sitelinks-all-lang.tsv \
     --split-en-sitelink-file ${DATADIR}/${WIKIDATA_ALL}-sitelinks-en-only.tsv \
     --split-property-edge-file ${DATADIR}/${WIKIDATA_ALL}-properties.tsv \
     --split-property-qual-file ${DATADIR}/${WIKIDATA_ALL}-property-qualifiers.tsv \
     --use-kgtkwriter True \
     --use-shm True \
     --procs 5 \
     --mapper-batch-size 5 \
     --max-size-per-mapper-queue 10 \
     --single-mapper-queue True \
     --collect-results True \
     --collect-seperately True\
     --collector-batch-size 10 \
     --collector-queue-per-proc-size 15 \
     --progress-interval 500000 \
    |& tee ${LOGDIR}/import-split-wikidata.log

# ==============================================================================
for TARGET in \
    ${WIKIDATA_ALL_NODES} \
	${WIKIDATA_ALL_EDGES}-full \
	${WIKIDATA_ALL_EDGES} \
	${WIKIDATA_ALL_QUALIFIERS}-full \
	${WIKIDATA_ALL_QUALIFIERS} \
	${WIKIDATA_ALL}-aliases-all-lang \
	${WIKIDATA_ALL}-aliases-en-only \
	${WIKIDATA_ALL}-descriptions-all-lang \
	${WIKIDATA_ALL}-descriptions-en-only \
	${WIKIDATA_ALL}-labels-all-lang \
	${WIKIDATA_ALL}-labels-en-only \
	${WIKIDATA_ALL}-datatypes \
	${WIKIDATA_ALL}-types \
	${WIKIDATA_ALL}-sitelinks-all-lang \
	${WIKIDATA_ALL}-sitelinks-en-only \
	${WIKIDATA_ALL}-properties \
	${WIKIDATA_ALL}-property-qualifiers
do
    echo -e "\nSort the ${TARGET} file."
    kgtk ${KGTK_FLAGS} \
	 sort2 ${VERBOSE} \
	 --input-file ${DATADIR}/${TARGET}.tsv \
	 --output-file ${DATADIR}/${TARGET}-sorted.tsv \
	 --extra "${SORT_EXTRAS}" \
	|& tee ${LOGDIR}/${TARGET}-sorted.log

    echo -e "\nCompress the sorted ${TARGET} file."
    time gzip --keep --force --verbose \
	 ${DATADIR}/${TARGET}-sorted.tsv \
	|& tee ${LOGDIR}/${TARGET}-compress.log

    echo -e "\nDeliver the compressed ${TARGET} file to the KGTK Google Drive."
    time rsync --archive --verbose \
	 ${DATADIR}/${TARGET}-sorted.tsv.gz \
	 ${PRODUCTDIR}/ \
	|& tee ${LOGDIR}/${TARGET}-deliver.log
done
