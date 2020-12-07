#! /bin/bash

source common.sh

# ==============================================================================
echo -e "\nCount the entities in the node1 column in ${DATADIR}/aliases.${SORTED_KGTK} and lift labels."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} --use-mgzip=${USE_MGZIP} --presorted \
     --input-file ${DATADIR}/aliases.${SORTED_KGTK} \
     --column node1 \
     --label node1-entity-count \
     / lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${DATADIR}/labels.${SORTED_KGTK} \
     --label-file-is-presorted \
     --output-file ${COUNTDIR}/aliases.node1.entity.counts.${SORTED_KGTK} \
     |& tee ${LOGDIR}/aliases.node1.entity.counts.log

echo -e "\nCount the entities in the node1 column in ${DATADIR}/descriptions.${SORTED_KGTK} and lift labels."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} --use-mgzip=${USE_MGZIP} --presorted \
     --input-file ${DATADIR}/descriptions.${SORTED_KGTK} \
     --column node1 \
     --label node1-entity-count \
     / lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${DATADIR}/labels.${SORTED_KGTK} \
     --label-file-is-presorted \
     --output-file ${COUNTDIR}/descriptions.node1.entity.counts.${SORTED_KGTK} \
     |& tee ${LOGDIR}/descriptions.node1.entity.counts.log

echo -e "\nCount the entities in the node1 column in ${DATADIR}/labels.${SORTED_KGTK} and lift labels."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} --use-mgzip=${USE_MGZIP} --presorted \
     --input-file ${DATADIR}/labels.${SORTED_KGTK} \
     --column node1 \
     --label node1-entity-count \
     / lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${DATADIR}/labels.${SORTED_KGTK} \
     --label-file-is-presorted \
     --output-file ${COUNTDIR}/labels.node1.entity.counts.${SORTED_KGTK} \
     |& tee ${LOGDIR}/labels.node1.entity.counts.log

echo -e "\nCount the entities in the node1 column in ${DATADIR}/sitelinks.${SORTED_KGTK} and lift labels."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} --use-mgzip=${USE_MGZIP} --presorted \
     --input-file ${DATADIR}/sitelinks.${SORTED_KGTK} \
     --column node1 \
     --label node1-entity-count \
     / lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${DATADIR}/labels.${SORTED_KGTK} \
     --label-file-is-presorted \
     --output-file ${COUNTDIR}/sitelinks.node1.entity.counts.${SORTED_KGTK} \
     |& tee ${LOGDIR}/sitelinks.node1.entity.counts.log
