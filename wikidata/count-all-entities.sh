#! /bin/bash

source common.sh

# ==============================================================================
echo -e "\nCount the entities in the node1 column in ${DATADIR}/all.${SORTED_KGTK}."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} \
     --input-file ${DATADIR}/all.${SORTED_KGTK} \
     --output-file ${DATADIR}/all.node1.entity.counts.${SORTED_KGTK} \
     --column node1 \
     --label node1-entity-count \
     --use-mgzip ${USE_MGZIP} \
     |& tee ${LOGDIR}/all.node1.entity.counts.log

echo -e "\nCount the entities in the label column in ${DATADIR}/all.${SORTED_KGTK}."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} \
     --input-file ${DATADIR}/all.${SORTED_KGTK} \
     --output-file ${DATADIR}/all.label.entity.counts.${SORTED_KGTK} \
     --column label \
     --label label-entity-count \
     --use-mgzip ${USE_MGZIP} \
     |& tee ${LOGDIR}/all.label.entity.counts.log

echo -e "\nCount the entities in the node2 column in ${DATADIR}/all.${SORTED_KGTK}."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} \
     --input-file ${DATADIR}/all.${SORTED_KGTK} \
     --output-file ${DATADIR}/all.node2.entity.counts.${SORTED_KGTK} \
     --column node2 \
     --label node2-entity-count \
     --use-mgzip ${USE_MGZIP} \
     |& tee ${LOGDIR}/all.node2.entity.counts.log
