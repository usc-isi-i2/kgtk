#! /bin/bash

source common.sh

# ==============================================================================
echo -e "\nCheck for claim entities without aliases."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${COUNTDIR}/claims.node1.entity.counts.${SORTED_KGTK} \
     --filter-file ${COUNTDIR}/aliases.node1.entity.counts.${SORTED_KGTK} \
     --output-file ${COUNTDIR}/claims.node1.entity.counts.unaliased.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1

echo -e "\nCheck for claim entities without descriptions."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${COUNTDIR}/claims.node1.entity.counts.${SORTED_KGTK} \
     --filter-file ${COUNTDIR}/descriptions.node1.entity.counts.${SORTED_KGTK} \
     --output-file ${COUNTDIR}/claims.node1.entity.counts.undescribed.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1

echo -e "\nCheck for claim entities without labels."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${COUNTDIR}/claims.node1.entity.counts.${SORTED_KGTK} \
     --filter-file ${COUNTDIR}/labels.node1.entity.counts.${SORTED_KGTK} \
     --output-file ${COUNTDIR}/claims.node1.entity.counts.unlabeled.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1

echo -e "\nCheck for claim entities without sitelinks."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${COUNTDIR}/claims.node1.entity.counts.${SORTED_KGTK} \
     --filter-file ${COUNTDIR}/sitelinks.node1.entity.counts.${SORTED_KGTK} \
     --output-file ${COUNTDIR}/claims.node1.entity.counts.unsitelinked.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1
