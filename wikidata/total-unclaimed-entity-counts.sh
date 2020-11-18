#! /bin/bash

source common.sh

# ==============================================================================
echo -e "\nTotal the unclaimed entity counts."
kgtk ${KGTK_FLAGS} \
     cat $VERBOSE --use-mgzip=$USE_MGZIP \
     --input-file ${DATADIR}/all.node1.entity.counts.unclaimed.${SORTED_KGTK} \
     --input-file ${DATADIR}/all.label.entity.counts.unclaimed.${SORTED_KGTK} \
     --input-file ${DATADIR}/all.node2.entity.counts.unclaimed.${SORTED_KGTK} \
     --output-file all.entity.counts.unclaimed.cat.${SORTED_KGTK}


kgtk ${KGTK_FLAGS} \
      unique $VERBOSE --use-mgzip=$USE_MGZIP \
     --input-file all.entity.counts.unclaimed.cat.${SORTED_KGTK} \
     --output-file all.entity.counts.unclaimed.slot.${SORTED_KGTK} \
     --column node1 \
     --label slot-count


kgtk ${KGTK_FLAGS} \
     lift $VERBOSE --use-mgzip=$USE_MGZIP \
     --input-file all.entity.counts.unclaimed.slot.${SORTED_KGTK} \
     --label-file ${DATADIR}/all.node1.entity.counts.unclaimed.${SORTED_KGTK} \
     --output-file all.entity.counts.unclaimed.slot.lift.node1.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --property node1-entity-count \
     --columns-to-write 'node1;node1-entity-count' \
     --input-file-is-presorted \
     --label-file-is-presorted


kgtk ${KGTK_FLAGS} \
     / lift $VERBOSE --use-mgzip=$USE_MGZIP \
     --input-file all.entity.counts.unclaimed.slot.lift.node1.${SORTED_KGTK} \
     --label-file ${DATADIR}/all.label.entity.counts.unclaimed.${SORTED_KGTK} \
     --output-file all.entity.counts.unclaimed.slot.lift.label.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --property label-entity-count \
     --columns-to-write 'node1;label-entity-count' \
     --input-file-is-presorted \
     --label-file-is-presorted


kgtk ${KGTK_FLAGS} \
     lift $VERBOSE --use-mgzip=$USE_MGZIP \
     --input-file all.entity.counts.unclaimed.slot.lift.label.${SORTED_KGTK} \
     --label-file ${DATADIR}/all.node2.entity.counts.unclaimed.${SORTED_KGTK} \
     --output-file all.entity.counts.unclaimed.slot.lift.node2.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --property node2-entity-count \
     --columns-to-write 'node1;node2-entity-count' \
     --input-file-is-presorted \
     --label-file-is-presorted


kgtk ${KGTK_FLAGS} \
     calc $VERBOSE --use-mgzip=$USE_MGZIP \
     --input-file all.entity.counts.unclaimed.slot.lift.node2.${SORTED_KGTK} \
     --output-file all.total.entity.counts.unclaimed.${SORTED_KGTK} \
     --columns 'node1;node1-entity-count' 'node1;label-entity-count' 'node1;node2-entity-count' \
     --do sum --into 'node1;total-entity-count'


