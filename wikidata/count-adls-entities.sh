#! /bin/bash

source common.sh

# ==============================================================================
echo -e "\nCount the entities in the node1 column in ${DATADIR}/aliases.${SORTED_KGTK}."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} \
     --input-file ${DATADIR}/aliases.${SORTED_KGTK} \
     --output-file ${DATADIR}/aliases.node1.entity.counts.${SORTED_KGTK} \
     --column node1 \
     --label node1-entity-count \
     --use-mgzip ${USE_MGZIP} \
     |& tee ${LOGDIR}/aliases.node1.entity.counts.log

echo -e "\nCount the entities in the node1 column in ${DATADIR}/descriptions.${SORTED_KGTK}."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} \
     --input-file ${DATADIR}/descriptions.${SORTED_KGTK} \
     --output-file ${DATADIR}/descriptions.node1.entity.counts.${SORTED_KGTK} \
     --column node1 \
     --label node1-entity-count \
     --use-mgzip ${USE_MGZIP} \
     |& tee ${LOGDIR}/descriptions.node1.entity.counts.log

echo -e "\nCount the entities in the node1 column in ${DATADIR}/labels.${SORTED_KGTK}."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} \
     --input-file ${DATADIR}/labels.${SORTED_KGTK} \
     --output-file ${DATADIR}/labels.node1.entity.counts.${SORTED_KGTK} \
     --column node1 \
     --label node1-entity-count \
     --use-mgzip ${USE_MGZIP} \
     |& tee ${LOGDIR}/labels.node1.entity.counts.log

echo -e "\nCount the entities in the node1 column in ${DATADIR}/sitelinks.${SORTED_KGTK}."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} \
     --input-file ${DATADIR}/sitelinks.${SORTED_KGTK} \
     --output-file ${DATADIR}/sitelinks.node1.entity.counts.${SORTED_KGTK} \
     --column node1 \
     --label node1-entity-count \
     --use-mgzip ${USE_MGZIP} \
     |& tee ${LOGDIR}/sitelinks.node1.entity.counts.log
