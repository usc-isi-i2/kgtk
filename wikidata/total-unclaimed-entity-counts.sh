#! /bin/bash

source common.sh

# ==============================================================================
echo -e "\nTotal the unclaimed entity counts."
kgtk ${KGTK_FLAGS} \
     cat $VERBOSE --use-mgzip=$USE_MGZIP \
     --input-file ${DATADIR}/all.node1.entity.counts.unclaimed.${SORTED_KGTK} \
     --input-file ${DATADIR}/all.label.entity.counts.unclaimed.${SORTED_KGTK} \
     --input-file ${DATADIR}/all.node2.entity.counts.unclaimed.${SORTED_KGTK} \
     / unique $VERBOSE --use-mgzip=$USE_MGZIP \
     --column node1 \
     / lift $VERBOSE --use-mgzip=$USE_MGZIP \
     --label-file ${DATADIR}/all.node1.entity.counts.unclaimed.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --property node1-entity-count \
     --columns-to-write 'node1;node1-entity-count' \
     --default-value 0 \
     --input-file-is-presorted \
     --label-file-is-presorted \
    / lift $VERBOSE --use-mgzip=$USE_MGZIP \
     --label-file ${DATADIR}/all.label.entity.counts.unclaimed.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --property label-entity-count \
     --columns-to-write 'node1;label-entity-count' \
     --default-value 0 \
     --input-file-is-presorted \
     --label-file-is-presorted \
     / lift $VERBOSE --use-mgzip=$USE_MGZIP \
     --label-file ${DATADIR}/all.node2.entity.counts.unclaimed.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --property node2-entity-count \
     --columns-to-write 'node1;node2-entity-count' \
     --default-value 0 \
     --input-file-is-presorted \
     --label-file-is-presorted \
     / calc $VERBOSE --use-mgzip=$USE_MGZIP \
     --columns 'node1;node1-entity-count' 'node1;label-entity-count' 'node1;node2-entity-count' \
     --do sum --into 'node1;total-entity-count' --format '%d' \
     / lift $VERBOSE --use-mgzip=$USE_MGZIP \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --input-file-is-presorted \
     --label-file-is-presorted \
     --output-file ${DATADIR}/all.total.entity.counts.unclaimed.${SORTED_KGTK}


