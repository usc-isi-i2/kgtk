#! /bin/bash

source common.sh

# ==============================================================================
echo -e "\nCheck for unclaimed properties in the node1 column."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${DATADIR}/all.node1.property.counts.${SORTED_KGTK} \
     --filter-file ${DATADIR}/claims.node1.property.counts.${SORTED_KGTK} \
     --output-file ${DATADIR}/all.node1.property.counts.unclaimed.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1

echo -e "\nCheck for unclaimed properties in the label column."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${DATADIR}/all.label.property.counts.${SORTED_KGTK} \
     --filter-file ${DATADIR}/claims.node1.property.counts.${SORTED_KGTK} \
     --output-file ${DATADIR}/all.label.property.counts.unclaimed.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1

echo -e "\nCheck for unclaimed properties in the node2 column."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${DATADIR}/all.node2.property.counts.${SORTED_KGTK} \
     --filter-file ${DATADIR}/claims.node1.property.counts.${SORTED_KGTK} \
     --output-file ${DATADIR}/all.node2.property.counts.unclaimed.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1
