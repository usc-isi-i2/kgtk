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
     --input-file ${DATADIR}/part.property.tsv \
     --output-file ${DATADIR}/property.datatype.tsv \
     --column "node2;wikidatatype" \
    |& tee ${LOGDIR}/${WIKIDATA_ALL}-property-datatypes.log

# ==============================================================================
# Split the properties by datatype.
echo -e "\nSplit ${DATADIR}/${WIKIDATA_ALL}-properties-sorted.tsv by datatype"
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/part.property.tsv \
     --obj "node2;wikidatatype" \
     --first-match-only \
     --pattern ";;commonsMedia" \
     --output-file ${DATADIR}/part-commonsMedia.tsv \
     --pattern ";;external-id" \
     --output-file ${DATADIR}/part.external-id.tsv \
     --pattern ";;math" \
     --output-file ${DATADIR}/part.math.tsv \
     --pattern ";;monolingualtext" \
     --output-file ${DATADIR}/part.monolingualtext.tsv \
     --pattern ";;quantity" \
     --output-file ${DATADIR}/part.quantity.tsv \
     --pattern ";;string" \
     --output-file ${DATADIR}/part.string.tsv \
     --pattern ";;time" \
     --output-file ${DATADIR}/part.time.tsv \
     --pattern ";;url" \
     --output-file ${DATADIR}/part.url.tsv \
     --pattern ";;wikibase-form" \
     --output-file ${DATADIR}/part.wikibase-form.tsv \
     --pattern ";;wikibase-item" \
     --output-file ${DATADIR}/part.wikibase-item.tsv \
     --pattern ";;wikibase-lexeme" \
     --output-file ${DATADIR}/part.wikibase-lexeme.tsv \
     --pattern ";;wikibase-property" \
     --output-file ${DATADIR}/part.wikibase-property.tsv \
     --pattern ";;wikibase-sense" \
     --output-file ${DATADIR}/part.wikibase-sense.tsv \
     --reject-file ${DATADIR}/part.other.tsv \
    |& tee ${LOGDIR}/property-datatype-split.log

# ==============================================================================
for TARGET in \
    commonsMedia \
	external-id \
	math \
	monolingualtext \
	quantity \
	string \
	time \
	url \
	wikibase-form \
	wikibase-item \
	wikibase-lexeme \
	wikibase-property \
	wikibase-sense \
	other
do
    TARGET_NAME=part.${TARGET}
    echo -e "\nCompress the sorted ${TARGET} file."
    time gzip --keep --force --verbose \
	 ${DATADIR}/${TARGET_NAME}.tsv \
	|& tee ${LOGDIR}/${TARGET_NAME}-compress.log

    echo -e "\nDeliver the compressed ${TARGET_NAME} file to the KGTK Google Drive."
    time rsync --archive --verbose \
	 ${DATADIR}/${TARGET_NAME}.tsv.gz \
	 ${PRODUCTDIR}/ \
	|& tee ${LOGDIR}/${TARGET_NAME}-deliver.log

    echo -e "\nExtract any qualifiers for the properties in ${TARGET_NAME}."
    kgtk ${KGTK_FLAGS} \
	 ifexists ${VERBOSE} \
	 --input-file ${DATADIR}/qual.tsv \
	 --filter-on ${DATADIR}/${TARGET_NAME}.tsv \
	 --output-file ${DATADIR}/${TARGET_NAME}.qual.tsv \
	 --input-keys node1 \
	 --filter-keys id \
	|& tee ${LOGDIR}/${TARGET_NAME}-qualifiers.log
	 
    echo -e "\nCompress the sorted qualifiers for the ${TARGET} properties."
    time gzip --keep --force --verbose \
	 ${DATADIR}/${TARGET_NAME}-.qual.tsv \
	|& tee ${LOGDIR}/${TARGET_NAME}-qualifiers-compress.log

    echo -e "\nDeliver the compressed qualifiers for ${TARGET_NAME} file to the KGTK Google Drive."
    time rsync --archive --verbose \
	 ${DATADIR}/${TARGET_NAME}.qual.tsv.gz \
	 ${PRODUCTDIR}/ \
	|& tee ${LOGDIR}/${TARGET_NAME}-qualifiers-deliver.log
done
