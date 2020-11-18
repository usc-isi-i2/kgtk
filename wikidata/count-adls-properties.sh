#! /bin/bash

source common.sh

# ==============================================================================
echo -e "\nCount the properties in the node1 column in ${DATADIR}/aliases.${SORTED_KGTK} and lift labels."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file ${DATADIR}/aliases.${SORTED_KGTK} \
     -p '^P[^-]*$ ;;' -o - \
     / unique ${VERBOSE} --use-mgzip=${USE_MGZIP} --presorted \
     --column node1 \
     --label node1-property-count \
     / lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --output-file ${DATADIR}/aliases.node1.property.counts.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --input-file-is-presorted \
     --label-file-is-presorted \
     |& tee ${LOGDIR}/aliases.node1.property.counts.log

echo -e "\nCount the properties in the node1 column in ${DATADIR}/descriptions.${SORTED_KGTK} and lift labels."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file ${DATADIR}/descriptions.${SORTED_KGTK} \
     -p '^P[^-]*$ ;;' -o - \
     / unique ${VERBOSE} --use-mgzip=${USE_MGZIP} --presorted \
     --column node1 \
     --label node1-property-count \
     / lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --output-file ${DATADIR}/descriptions.node1.property.counts.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --input-file-is-presorted \
     --label-file-is-presorted \
     |& tee ${LOGDIR}/descriptions.node1.property.counts.log

echo -e "\nCount the properties in the node1 column in ${DATADIR}/labels.${SORTED_KGTK} and lift labels."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file ${DATADIR}/labels.${SORTED_KGTK} \
     -p '^P[^-]*$ ;;' -o - \
     / unique ${VERBOSE} --use-mgzip=${USE_MGZIP} --presorted \
     --column node1 \
     --label node1-property-count \
     / lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --output-file ${DATADIR}/labels.node1.property.counts.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --input-file-is-presorted \
     --label-file-is-presorted \
     |& tee ${LOGDIR}/labels.node1.property.counts.log

echo -e "\nCount the properties in the node1 column in ${DATADIR}/sitelinks.${SORTED_KGTK} and lift labels."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file ${DATADIR}/sitelinks.${SORTED_KGTK} \
     -p '^P[^-]*$ ;;' -o - \
     / unique ${VERBOSE} --use-mgzip=${USE_MGZIP} --presorted \
     --column node1 \
     --label node1-property-count \
     / lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --output-file ${DATADIR}/sitelinks.node1.property.counts.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --input-file-is-presorted \
     --label-file-is-presorted \
     |& tee ${LOGDIR}/sitelinks.node1.property.counts.log
