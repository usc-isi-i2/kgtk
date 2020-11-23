#! /bin/bash

source common.sh

# ==============================================================================
echo -e "\nTotal the unclaimed property counts."
kgtk ${KGTK_FLAGS} \
     cat $VERBOSE --use-mgzip=$USE_MGZIP \
     --input-file ${COUNTDIR}/all.node1.property.counts.unclaimed.${SORTED_KGTK} \
     --input-file ${COUNTDIR}/all.label.property.counts.unclaimed.${SORTED_KGTK} \
     --input-file ${COUNTDIR}/all.node2.property.counts.unclaimed.${SORTED_KGTK} \
     / unique $VERBOSE --use-mgzip=$USE_MGZIP \
     --column node1 \
     / lift $VERBOSE --use-mgzip=$USE_MGZIP \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${COUNTDIR}/all.node1.property.counts.unclaimed.${SORTED_KGTK} \
     --label-file-is-presorted \
     --property node1-property-count \
     --columns-to-write 'node1;node1-property-count' \
     --default-value 0 \
     / lift $VERBOSE --use-mgzip=$USE_MGZIP \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${COUNTDIR}/all.label.property.counts.unclaimed.${SORTED_KGTK} \
     --label-file-is-presorted \
     --property label-property-count \
     --columns-to-write 'node1;label-property-count' \
     --default-value 0 \
     / lift $VERBOSE --use-mgzip=$USE_MGZIP \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${COUNTDIR}/all.node2.property.counts.unclaimed.${SORTED_KGTK} \
     --label-file-is-presorted \
     --property node2-property-count \
     --columns-to-write 'node1;node2-property-count' \
     --default-value 0 \
     / calc $VERBOSE --use-mgzip=$USE_MGZIP \
     --columns 'node1;node1-property-count' 'node1;label-property-count' 'node1;node2-property-count' \
     --do sum --into 'node1;total-property-count' --format '%d' \
     / lift $VERBOSE --use-mgzip=$USE_MGZIP \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --label-file-is-presorted \
     --output-file ${COUNTDIR}/all.total.property.counts.unclaimed.${SORTED_KGTK}
