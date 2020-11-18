#! /bin/bash

source common.sh

# ==============================================================================
echo -e "\nCheck for unclaimed alias entities."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${DATADIR}/aliases.node1.entity.counts.${SORTED_KGTK} \
     --filter-file ${DATADIR}/claims.node1.entity.counts.${SORTED_KGTK} \
     --output-file ${DATADIR}/aliases.node1.entity.counts.unclaimed.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1

echo -e "\nCheck for unclaimed description entities."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${DATADIR}/descriptions.node1.entity.counts.${SORTED_KGTK} \
     --filter-file ${DATADIR}/claims.node1.entity.counts.${SORTED_KGTK} \
     --output-file ${DATADIR}/descriptions.node1.entity.counts.unclaimed.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1

echo -e "\nCheck for unclaimed label entities."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${DATADIR}/labels.node1.entity.counts.${SORTED_KGTK} \
     --filter-file ${DATADIR}/claims.node1.entity.counts.${SORTED_KGTK} \
     --output-file ${DATADIR}/labels.node1.entity.counts.unclaimed.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1

echo -e "\nCheck for unclaimed sitelink entities."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${DATADIR}/sitelinks.node1.entity.counts.${SORTED_KGTK} \
     --filter-file ${DATADIR}/claims.node1.entity.counts.${SORTED_KGTK} \
     --output-file ${DATADIR}/sitelinks.node1.entity.counts.unclaimed.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1
