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
# Split the edges by datatype.
echo -e "\nSplit ${DATADIR}/${WIKIDATA_ALL}-properties-sorted.tsv by datatype"
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/parttsv \
     --obj "node2;wikidatatype" \
     --first-match-only \
     --pattern ";;commonsMedia" \
     --output-file ${DATADIR}/part.commonsMedia.tsv \
     --pattern ";;external-id" \
     --output-file ${DATADIR}/part.external-id.tsv \
     --pattern ";;geo-shape" \
     --output-file ${DATADIR}/part.geo-shape.tsv \
     --pattern ";;globe-coordinate" \
     --output-file ${DATADIR}/part.globe-coordinate.tsv \
     --pattern ";;math" \
     --output-file ${DATADIR}/part.math.tsv \
     --pattern ";;monolingualtext" \
     --output-file ${DATADIR}/part.monolingualtext.tsv \
     --pattern ";;musical-notation" \
     --output-file ${DATADIR}/part.musical-notation.tsv \
     --pattern ";;quantity" \
     --output-file ${DATADIR}/part.quantity.tsv \
     --pattern ";;string" \
     --output-file ${DATADIR}/part.string.tsv \
     --pattern ";;tabular-data" \
     --output-file ${DATADIR}/part.tabular-data.tsv \
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
    |& tee ${LOGDIR}/edge-datatype-split.log

# ==============================================================================
# Compress and deliver the edge datatypes.
for TARGET in ${WIKIDATATYPES[@]}
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
	|& tee ${LOGDIR}/${TARGET_NAME}.qual.log
	 
    echo -e "\nCompress the sorted qualifiers for the ${TARGET} properties."
    time gzip --keep --force --verbose \
	 ${DATADIR}/${TARGET_NAME}.qual.tsv \
	|& tee ${LOGDIR}/${TARGET_NAME}.qual-compress.log

    echo -e "\nDeliver the compressed qualifiers for ${TARGET_NAME} file to the KGTK Google Drive."
    time rsync --archive --verbose \
	 ${DATADIR}/${TARGET_NAME}.qual.tsv.gz \
	 ${PRODUCTDIR}/ \
	|& tee ${LOGDIR}/${TARGET_NAME}.qual-deliver.log
done
