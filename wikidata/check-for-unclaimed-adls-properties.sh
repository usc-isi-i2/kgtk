#! /bin/bash

source common.sh

# ==============================================================================
echo -e "\nCheck for unclaimed alias properties."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${DATADIR}/aliases.node1.property.counts.${SORTED_KGTK} \
     --filter-file ${DATADIR}/claims.node1.property.counts.${SORTED_KGTK} \
     --output-file ${DATADIR}/aliases.node1.property.counts.unclaimed.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1

echo -e "\nCheck for unclaimed description properties."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${DATADIR}/descriptions.node1.property.counts.${SORTED_KGTK} \
     --filter-file ${DATADIR}/claims.node1.property.counts.${SORTED_KGTK} \
     --output-file ${DATADIR}/descriptions.node1.property.counts.unclaimed.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1

echo -e "\nCheck for unclaimed label properties."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${DATADIR}/labels.node1.property.counts.${SORTED_KGTK} \
     --filter-file ${DATADIR}/claims.node1.property.counts.${SORTED_KGTK} \
     --output-file ${DATADIR}/labels.node1.property.counts.unclaimed.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1

echo -e "\nCheck for unclaimed sitelink properties."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${DATADIR}/sitelinks.node1.property.counts.${SORTED_KGTK} \
     --filter-file ${DATADIR}/claims.node1.property.counts.${SORTED_KGTK} \
     --output-file ${DATADIR}/sitelinks.node1.property.counts.unclaimed.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1
