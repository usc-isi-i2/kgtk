#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Split the edges by datatype.
echo -e "\nSplit ${DATADIR}/${WIKIDATA_ALL}-properties-sorted.tsv by datatype"
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/all.${SORTED_KGTK} \
     --obj "node2;wikidatatype" \
     --first-match-only \
     --pattern ";;commonsMedia" \
     --output-file ${DATADIR}/part.commonsMedia.${SORTED_KGTK} \
     --pattern ";;external-id" \
     --output-file ${DATADIR}/part.external-id.${SORTED_KGTK} \
     --pattern ";;geo-shape" \
     --output-file ${DATADIR}/part.geo-shape.${SORTED_KGTK} \
     --pattern ";;globe-coordinate" \
     --output-file ${DATADIR}/part.globe-coordinate.${SORTED_KGTK} \
     --pattern ";;math" \
     --output-file ${DATADIR}/part.math.${SORTED_KGTK} \
     --pattern ";;monolingualtext" \
     --output-file ${DATADIR}/part.monolingualtext.${SORTED_KGTK} \
     --pattern ";;musical-notation" \
     --output-file ${DATADIR}/part.musical-notation.${SORTED_KGTK} \
     --pattern ";;quantity" \
     --output-file ${DATADIR}/part.quantity.${SORTED_KGTK} \
     --pattern ";;string" \
     --output-file ${DATADIR}/part.string.${SORTED_KGTK} \
     --pattern ";;tabular-data" \
     --output-file ${DATADIR}/part.tabular-data.${SORTED_KGTK} \
     --pattern ";;time" \
     --output-file ${DATADIR}/part.time.${SORTED_KGTK} \
     --pattern ";;url" \
     --output-file ${DATADIR}/part.url.${SORTED_KGTK} \
     --pattern ";;wikibase-form" \
     --output-file ${DATADIR}/part.wikibase-form.${SORTED_KGTK} \
     --pattern ";;wikibase-item" \
     --output-file ${DATADIR}/part.wikibase-item.${SORTED_KGTK} \
     --pattern ";;wikibase-lexeme" \
     --output-file ${DATADIR}/part.wikibase-lexeme.${SORTED_KGTK} \
     --pattern ";;wikibase-property" \
     --output-file ${DATADIR}/part.wikibase-property.${SORTED_KGTK} \
     --pattern ";;wikibase-sense" \
     --output-file ${DATADIR}/part.wikibase-sense.${SORTED_KGTK} \
     --reject-file ${DATADIR}/part.other.${SORTED_KGTK} \
     --use-mgzip ${USE_MGZIP} \
    |& tee ${LOGDIR}/edge-datatype-split.log
