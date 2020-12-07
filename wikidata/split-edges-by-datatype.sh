#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Split the edges by datatype.
echo -e "\nSplit ${DATADIR}/claims.${SORTED_KGTK} by datatype"
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/claims.${SORTED_KGTK} \
     --obj "node2;wikidatatype" \
     --first-match-only \
     --pattern ";;commonsMedia" \
     --output-file ${DATADIR}/claims.commonsMedia.${SORTED_KGTK} \
     --pattern ";;external-id" \
     --output-file ${DATADIR}/claims.external-id.${SORTED_KGTK} \
     --pattern ";;geo-shape" \
     --output-file ${DATADIR}/claims.geo-shape.${SORTED_KGTK} \
     --pattern ";;globe-coordinate" \
     --output-file ${DATADIR}/claims.globe-coordinate.${SORTED_KGTK} \
     --pattern ";;math" \
     --output-file ${DATADIR}/claims.math.${SORTED_KGTK} \
     --pattern ";;monolingualtext" \
     --output-file ${DATADIR}/claims.monolingualtext.${SORTED_KGTK} \
     --pattern ";;musical-notation" \
     --output-file ${DATADIR}/claims.musical-notation.${SORTED_KGTK} \
     --pattern ";;quantity" \
     --output-file ${DATADIR}/claims.quantity.${SORTED_KGTK} \
     --pattern ";;string" \
     --output-file ${DATADIR}/claims.string.${SORTED_KGTK} \
     --pattern ";;tabular-data" \
     --output-file ${DATADIR}/claims.tabular-data.${SORTED_KGTK} \
     --pattern ";;time" \
     --output-file ${DATADIR}/claims.time.${SORTED_KGTK} \
     --pattern ";;url" \
     --output-file ${DATADIR}/claims.url.${SORTED_KGTK} \
     --pattern ";;wikibase-form" \
     --output-file ${DATADIR}/claims.wikibase-form.${SORTED_KGTK} \
     --pattern ";;wikibase-item" \
     --output-file ${DATADIR}/claims.wikibase-item.${SORTED_KGTK} \
     --pattern ";;wikibase-lexeme" \
     --output-file ${DATADIR}/claims.wikibase-lexeme.${SORTED_KGTK} \
     --pattern ";;wikibase-property" \
     --output-file ${DATADIR}/claims.wikibase-property.${SORTED_KGTK} \
     --pattern ";;wikibase-sense" \
     --output-file ${DATADIR}/claims.wikibase-sense.${SORTED_KGTK} \
     --reject-file ${DATADIR}/claims.other.${SORTED_KGTK} \
     --use-mgzip ${USE_MGZIP} \
    |& tee ${LOGDIR}/edge-datatype-split.log
