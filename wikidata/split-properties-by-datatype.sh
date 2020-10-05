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
# Count the property datatypes.
echo -e "\nCount unique datatypes in ${DATADIR}/${WIKIDATA_ALL}-properties.tsv"
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL}-properties.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-property-datatypes.tsv \
     --column "node2;wikidatatype" \
    |& tee ${LOGDIR}/${WIKIDATA_ALL}-property-datatypes.log

# ==============================================================================
# Split the properties by datatype.
echo -e "\nSplit ${DATADIR}/${WIKIDATA_ALL}-properties-sorted.tsv by datatype"
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL}-properties-sorted.tsv \
     --obj "node2;wikidatatype" \
     --first-match-only \
     --pattern ";;commonsMedia" \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-property-commonsMedia-sorted.tsv \
     --pattern ";;external-id" \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-property-external-id-sorted.tsv \
     --pattern ";;math" \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-property-math-sorted.tsv \
     --pattern ";;monolingualtext" \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-property-monolingualtext-sorted.tsv \
     --pattern ";;quantity" \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-property-quantity-sorted.tsv \
     --pattern ";;string" \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-property-string-sorted.tsv \
     --pattern ";;time" \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-property-time-sorted.tsv \
     --pattern ";;url" \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-property-url-sorted.tsv \
     --pattern ";;wikibase-form" \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-property-wikibase-form-sorted.tsv \
     --pattern ";;wikibase-item" \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-property-wikibase-item-sorted.tsv \
     --pattern ";;wikibase-lexeme" \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-property-wikibase-lexeme-sorted.tsv \
     --pattern ";;wikibase-property" \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-property-wikibase-property-sorted.tsv \
     --pattern ";;wikibase-sense" \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-property-wikibase-sense-sorted.tsv \
     --reject-file ${DATADIR}/${WIKIDATA_ALL}-property-other-sorted.tsv \
    |& tee ${LOGDIR}/${WIKIDATA_ALL}-property-datatype-split.log

