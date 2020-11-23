#! /bin/bash

source common.sh

# ==============================================================================
echo -e "\nCount the entities in the node1 column in ${DATADIR}/aliases.en.${SORTED_KGTK} and lift labels."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} --use-mgzip=${USE_MGZIP} --presorted \
     --input-file ${DATADIR}/aliases.en.${SORTED_KGTK} \
     --column node1 \
     --label node1-entity-count \
     / lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --label-file-is-presorted \
     --output-file ${COUNTDIR}/aliases.en.node1.entity.counts.${SORTED_KGTK} \
     |& tee ${LOGDIR}/aliases.en.node1.entity.counts.log

echo -e "\nCount the entities in the node1 column in ${DATADIR}/descriptions.en.${SORTED_KGTK} and lift labels."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} --use-mgzip=${USE_MGZIP} --presorted \
     --input-file ${DATADIR}/descriptions.en.${SORTED_KGTK} \
     --column node1 \
     --label node1-entity-count \
     / lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --label-file-is-presorted \
     --output-file ${COUNTDIR}/descriptions.en.node1.entity.counts.${SORTED_KGTK} \
     |& tee ${LOGDIR}/descriptions.en.node1.entity.counts.log

echo -e "\nCount the entities in the node1 column in ${DATADIR}/labels.en.${SORTED_KGTK} and lift labels."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} --use-mgzip=${USE_MGZIP} --presorted \
     --input-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --column node1 \
     --label node1-entity-count \
     / lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --label-file-is-presorted \
     --output-file ${COUNTDIR}/labels.en.node1.entity.counts.${SORTED_KGTK} \
     |& tee ${LOGDIR}/labels.en.node1.entity.counts.log

echo -e "\nCount the entities in the node1 column in ${DATADIR}/sitelinks.en.${SORTED_KGTK} and lift labels."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} --use-mgzip=${USE_MGZIP} --presorted \
     --input-file ${DATADIR}/sitelinks.en.${SORTED_KGTK} \
     --column node1 \
     --label node1-entity-count \
     / lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --label-file-is-presorted \
     --output-file ${COUNTDIR}/sitelinks.en.node1.entity.counts.${SORTED_KGTK} \
     |& tee ${LOGDIR}/sitelinks.en.node1.entity.counts.log
