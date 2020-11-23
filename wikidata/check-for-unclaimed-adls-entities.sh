#! /bin/bash

source common.sh

# ==============================================================================
echo -e "\nCheck for unclaimed alias entities."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${COUNTDIR}/aliases.node1.entity.counts.${SORTED_KGTK} \
     --filter-file ${COUNTDIR}/claims.node1.entity.counts.${SORTED_KGTK} \
     --output-file ${COUNTDIR}/aliases.node1.entity.counts.unclaimed.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1

echo -e "\nCheck for unclaimed description entities."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${COUNTDIR}/descriptions.node1.entity.counts.${SORTED_KGTK} \
     --filter-file ${COUNTDIR}/claims.node1.entity.counts.${SORTED_KGTK} \
     --output-file ${COUNTDIR}/descriptions.node1.entity.counts.unclaimed.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1

echo -e "\nCheck for unclaimed label entities."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${COUNTDIR}/labels.node1.entity.counts.${SORTED_KGTK} \
     --filter-file ${COUNTDIR}/claims.node1.entity.counts.${SORTED_KGTK} \
     --output-file ${COUNTDIR}/labels.node1.entity.counts.unclaimed.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1

echo -e "\nCheck for unclaimed sitelink entities."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${COUNTDIR}/sitelinks.node1.entity.counts.${SORTED_KGTK} \
     --filter-file ${COUNTDIR}/claims.node1.entity.counts.${SORTED_KGTK} \
     --output-file ${COUNTDIR}/sitelinks.node1.entity.counts.unclaimed.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1
