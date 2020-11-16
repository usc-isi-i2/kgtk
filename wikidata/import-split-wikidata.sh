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
     --node-file ${DATADIR}/node.unsorted.tsv \
     --detailed-edge-file ${DATADIR}/all.full.unsorted.tsv \
     --minimal-edge-file ${DATADIR}/all.unsorted.tsv \
     --detailed-qual-file ${DATADIR}/qual.full.unsorted.tsv \
     --minimal-qual-file ${DATADIR}/qual.unsorted.tsv \
     --node-file-id-only \
     --explode-values False \
     --all-languages \
     --alias-edges True \
     --split-alias-file ${DATADIR}/part.alias.unsorted.tsv \
     --split-en-alias-file ${DATADIR}/part.alias.en.unsorted.tsv \
     --description-edges True \
     --split-description-file ${DATADIR}/part.description.unsorted.tsv \
     --split-en-description-file ${DATADIR}/part.description.en.unsorted.tsv \
     --label-edges True \
     --split-label-file ${DATADIR}/part.label.unsorted.tsv \
     --split-en-label-file ${DATADIR}/part.label.en.unsorted.tsv \
     --datatype-edges True \
     --split-datatype-file ${DATADIR}/property.datatype.unsorted.tsv \
     --entry-type-edges True \
     --split-type-file ${DATADIR}/types.unsorted.tsv \
     --sitelink-edges True \
     --sitelink-verbose-edges True \
     --split-sitelink-file ${DATADIR}/part.wikipedia_sitelink.unsorted.tsv \
     --split-en-sitelink-file ${DATADIR}/part.wikipedia_sitelink.en.unsorted.tsv \
     --split-property-edge-file ${DATADIR}/part.property.unsorted.tsv \
     --split-property-qual-file ${DATADIR}/part.property.qual.unsorted.tsv \
     --value-hash-width 6 \
     --claim-id-hash-width 8 \
     --use-kgtkwriter True \
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

# ==============================================================================
for TARGET in \
    node \
	all.full \
	all \
	qual.full \
	qual \
	part.alias \
	part.alias.en \
	part.description \
	part.description.en \
	part.label \
	part.label.en \
	property.datatype \
	types \
	part.wikipedia_sitelink \
	part.wikipedia_sitelink.en \
	part.property \
	part.property.qual \
do
    echo -e "\nSort the ${TARGET} file."
    kgtk ${KGTK_FLAGS} \
	 sort2 ${VERBOSE} \
	 --input-file ${DATADIR}/${TARGET}.unsorted.tsv \
	 --output-file ${DATADIR}/${TARGET}.tsv \
	 --extra "${SORT_EXTRAS}" \
	|& tee ${LOGDIR}/${TARGET}-sorted.log

    echo -e "\nCompress the sorted ${TARGET} file."
    time gzip --keep --force --verbose \
	 ${DATADIR}/${TARGET}.tsv \
	|& tee ${LOGDIR}/${TARGET}-compress.log

    echo -e "\nDeliver the compressed ${TARGET} file to the KGTK Google Drive."
    time rsync --archive --verbose \
	 ${DATADIR}/${TARGET}.tsv.gz \
	 ${PRODUCTDIR}/ \
	|& tee ${LOGDIR}/${TARGET}-deliver.log
done
