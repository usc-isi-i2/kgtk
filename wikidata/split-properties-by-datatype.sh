#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Split the properties by datatype.
echo -e "\nSplit ${DATADIR}/part.property.tsv by datatype"
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/part.property.tsv \
     --obj "node2;wikidatatype" \
     --first-match-only \
     --pattern ";;commonsMedia" \
     --output-file ${DATADIR}/part.property.commonsMedia.tsv \
     --pattern ";;external-id" \
     --output-file ${DATADIR}/part.property.external-id.tsv \
     --pattern ";;geo-shape" \
     --output-file ${DATADIR}/part.property.geo-shape.tsv \
     --pattern ";;globe-coordinate" \
     --output-file ${DATADIR}/part.property.globe-coordinate.tsv \
     --pattern ";;math" \
     --output-file ${DATADIR}/part.property.math.tsv \
     --pattern ";;monolingualtext" \
     --output-file ${DATADIR}/part.property.monolingualtext.tsv \
     --pattern ";;musical-notation" \
     --output-file ${DATADIR}/part.property.musical-notation.tsv \
     --pattern ";;quantity" \
     --output-file ${DATADIR}/part.property.quantity.tsv \
     --pattern ";;string" \
     --output-file ${DATADIR}/part.property.string.tsv \
     --pattern ";;tabular-data" \
     --output-file ${DATADIR}/part.property.tabular-data.tsv \
     --pattern ";;time" \
     --output-file ${DATADIR}/part.property.time.tsv \
     --pattern ";;url" \
     --output-file ${DATADIR}/part.property.url.tsv \
     --pattern ";;wikibase-form" \
     --output-file ${DATADIR}/part.property.wikibase-form.tsv \
     --pattern ";;wikibase-item" \
     --output-file ${DATADIR}/part.property.wikibase-item.tsv \
     --pattern ";;wikibase-lexeme" \
     --output-file ${DATADIR}/part.property.wikibase-lexeme.tsv \
     --pattern ";;wikibase-property" \
     --output-file ${DATADIR}/part.property.wikibase-property.tsv \
     --pattern ";;wikibase-sense" \
     --output-file ${DATADIR}/part.property.wikibase-sense.tsv \
     --reject-file ${DATADIR}/part.property.other.tsv \
    |& tee ${LOGDIR}/property-datatype-split.log
