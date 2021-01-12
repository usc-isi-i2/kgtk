#! /bin/bash

source common.sh

# ==============================================================================
echo -e "\nCheck for unclaimed alias properties."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${COUNTDIR}/aliases.node1.property.counts.${SORTED_KGTK} \
     --filter-file ${COUNTDIR}/claims.node1.property.counts.${SORTED_KGTK} \
     --output-file ${COUNTDIR}/aliases.node1.property.counts.unclaimed.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1

echo -e "\nCheck for unclaimed description properties."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${COUNTDIR}/descriptions.node1.property.counts.${SORTED_KGTK} \
     --filter-file ${COUNTDIR}/claims.node1.property.counts.${SORTED_KGTK} \
     --output-file ${COUNTDIR}/descriptions.node1.property.counts.unclaimed.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1

echo -e "\nCheck for unclaimed label properties."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${COUNTDIR}/labels.node1.property.counts.${SORTED_KGTK} \
     --filter-file ${COUNTDIR}/claims.node1.property.counts.${SORTED_KGTK} \
     --output-file ${COUNTDIR}/labels.node1.property.counts.unclaimed.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1

echo -e "\nCheck for unclaimed sitelink properties."
kgtk ${KGTK_FLAGS} \
     ifnotexists $VERBOSE --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${COUNTDIR}/sitelinks.node1.property.counts.${SORTED_KGTK} \
     --filter-file ${COUNTDIR}/claims.node1.property.counts.${SORTED_KGTK} \
     --output-file ${COUNTDIR}/sitelinks.node1.property.counts.unclaimed.${SORTED_KGTK} \
     --input-keys node1 \
     --filter-keys node1
