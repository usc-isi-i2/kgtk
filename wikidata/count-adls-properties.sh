#! /bin/bash

source common.sh

# ==============================================================================
echo -e "\nCount the properties in the node1 column in ${DATADIR}/aliases.${SORTED_KGTK} and lift labels."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file ${DATADIR}/aliases.${SORTED_KGTK} \
     -p '^P ;;' -o - \
     / unique ${VERBOSE} --use-mgzip=${USE_MGZIP} --presorted \
     --column node1 \
     --label node1-property-count \
     / lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --label-file-is-presorted \
     --output-file ${COUNTDIR}/aliases.node1.property.counts.${SORTED_KGTK} \
     |& tee ${LOGDIR}/aliases.node1.property.counts.log

echo -e "\nCount the properties in the node1 column in ${DATADIR}/descriptions.${SORTED_KGTK} and lift labels."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file ${DATADIR}/descriptions.${SORTED_KGTK} \
     -p '^P ;;' -o - \
     / unique ${VERBOSE} --use-mgzip=${USE_MGZIP} --presorted \
     --column node1 \
     --label node1-property-count \
     / lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --label-file-is-presorted \
     --output-file ${COUNTDIR}/descriptions.node1.property.counts.${SORTED_KGTK} \
     |& tee ${LOGDIR}/descriptions.node1.property.counts.log

echo -e "\nCount the properties in the node1 column in ${DATADIR}/labels.${SORTED_KGTK} and lift labels."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file ${DATADIR}/labels.${SORTED_KGTK} \
     -p '^P ;;' -o - \
     / unique ${VERBOSE} --use-mgzip=${USE_MGZIP} --presorted \
     --column node1 \
     --label node1-property-count \
     / lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --label-file-is-presorted \
     --output-file ${COUNTDIR}/labels.node1.property.counts.${SORTED_KGTK} \
     |& tee ${LOGDIR}/labels.node1.property.counts.log

echo -e "\nCount the properties in the node1 column in ${DATADIR}/sitelinks.${SORTED_KGTK} and lift labels."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file ${DATADIR}/sitelinks.${SORTED_KGTK} \
     -p '^P ;;' -o - \
     / unique ${VERBOSE} --use-mgzip=${USE_MGZIP} --presorted \
     --column node1 \
     --label node1-property-count \
     / lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --label-file-is-presorted \
     --output-file ${COUNTDIR}/sitelinks.node1.property.counts.${SORTED_KGTK} \
     |& tee ${LOGDIR}/sitelinks.node1.property.counts.log
