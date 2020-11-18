#! /bin/bash

source common.sh

# ==============================================================================
echo -e "\nTotal the property counts."
kgtk ${KGTK_FLAGS} \
     cat $VERBOSE --use-mgzip=$USE_MGZIP \
     --input-file ${DATADIR}/all.node1.property.counts.${SORTED_KGTK} \
     --input-file ${DATADIR}/all.label.property.counts.${SORTED_KGTK} \
     --input-file ${DATADIR}/all.node2.property.counts.${SORTED_KGTK} \
     / unique $VERBOSE --use-mgzip=$USE_MGZIP \
     --column node1 \
     --label slot-count \
     / lift $VERBOSE --use-mgzip=$USE_MGZIP \
     --label-file ${DATADIR}/all.node1.property.counts.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --property node1-property-count \
     --input-file-is-presorted \
     --label-file-is-presorted \
     / lift $VERBOSE --use-mgzip=$USE_MGZIP \
     --label-file ${DATADIR}/all.label.property.counts.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --property label-property-count \
     --input-file-is-presorted \
     --label-file-is-presorted \
     / lift $VERBOSE --use-mgzip=$USE_MGZIP \
     --label-file ${DATADIR}/all.node2.property.counts.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --property node2-property-count \
     --input-file-is-presorted \
     --label-file-is-presorted \
     / calc $VERBOSE --use-mgzip=$USE_MGZIP \
     --columns 'node1;node1-property-count' 'node1;label-property-count' 'node1;node2-property-count' \
     --do sum --into 'node1;total-property-count' \
     --output-file ${DATADIR}/all.total.property.counts.${SORTED_KGTK}
