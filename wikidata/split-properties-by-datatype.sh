#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Split the properties by datatype.
echo -e "\nSplit ${DATADIR}/part.property.${SORTED_KGTK} by datatype"
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/part.property.${SORTED_KGTK} \
     --obj "node2;wikidatatype" \
     --first-match-only \
     --pattern ";;commonsMedia" \
     --output-file ${DATADIR}/part.property.commonsMedia.${SORTED_KGTK} \
     --pattern ";;external-id" \
     --output-file ${DATADIR}/part.property.external-id.${SORTED_KGTK} \
     --pattern ";;geo-shape" \
     --output-file ${DATADIR}/part.property.geo-shape.${SORTED_KGTK} \
     --pattern ";;globe-coordinate" \
     --output-file ${DATADIR}/part.property.globe-coordinate.${SORTED_KGTK} \
     --pattern ";;math" \
     --output-file ${DATADIR}/part.property.math.${SORTED_KGTK} \
     --pattern ";;monolingualtext" \
     --output-file ${DATADIR}/part.property.monolingualtext.${SORTED_KGTK} \
     --pattern ";;musical-notation" \
     --output-file ${DATADIR}/part.property.musical-notation.${SORTED_KGTK} \
     --pattern ";;quantity" \
     --output-file ${DATADIR}/part.property.quantity.${SORTED_KGTK} \
     --pattern ";;string" \
     --output-file ${DATADIR}/part.property.string.${SORTED_KGTK} \
     --pattern ";;tabular-data" \
     --output-file ${DATADIR}/part.property.tabular-data.${SORTED_KGTK} \
     --pattern ";;time" \
     --output-file ${DATADIR}/part.property.time.${SORTED_KGTK} \
     --pattern ";;url" \
     --output-file ${DATADIR}/part.property.url.${SORTED_KGTK} \
     --pattern ";;wikibase-form" \
     --output-file ${DATADIR}/part.property.wikibase-form.${SORTED_KGTK} \
     --pattern ";;wikibase-item" \
     --output-file ${DATADIR}/part.property.wikibase-item.${SORTED_KGTK} \
     --pattern ";;wikibase-lexeme" \
     --output-file ${DATADIR}/part.property.wikibase-lexeme.${SORTED_KGTK} \
     --pattern ";;wikibase-property" \
     --output-file ${DATADIR}/part.property.wikibase-property.${SORTED_KGTK} \
     --pattern ";;wikibase-sense" \
     --output-file ${DATADIR}/part.property.wikibase-sense.${SORTED_KGTK} \
     --reject-file ${DATADIR}/part.property.other.${SORTED_KGTK} \
     --use-mgzip ${USE_MGZIP} \
    |& tee ${LOGDIR}/property-datatype-split.log
