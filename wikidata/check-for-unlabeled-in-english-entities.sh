#! /bin/bash

source common.sh

# ==============================================================================
echo -e "\nCheck for unlabeled entities in the node1 column."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${DATADIR}/all.node1.entity.counts.${SORTED_KGTK} \
     --filter-file ${DATADIR}/labels.en.node1.entity.counts.${SORTED_KGTK} \
     --output-file ${DATADIR}/all.node1.entity.counts.unlabeled.en.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1

echo -e "\nCheck for unlabeled entities in the label column."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${DATADIR}/all.label.entity.counts.${SORTED_KGTK} \
     --filter-file ${DATADIR}/labels.en.node1.entity.counts.${SORTED_KGTK} \
     --output-file ${DATADIR}/all.label.entity.counts.unlabeled.en.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1

echo -e "\nCheck for unlabeled entities in the node2 column."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${DATADIR}/all.node2.entity.counts.${SORTED_KGTK} \
     --filter-file ${DATADIR}/labels.en.node1.entity.counts.${SORTED_KGTK} \
     --output-file ${DATADIR}/all.node2.entity.counts.unlabeled.en.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1
