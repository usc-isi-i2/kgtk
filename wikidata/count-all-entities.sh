#! /bin/bash

source common.sh

# ==============================================================================
echo -e "\nCount the entities in the node1 column in ${DATADIR}/all.${SORTED_KGTK} and lift English labels."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file ${DATADIR}/all.${SORTED_KGTK} \
     -p '^[PQ][^-]*$ ;;' -o - \
     / unique ${VERBOSE} \
     --column node1 \
     --label node1-entity-count \
     --use-mgzip ${USE_MGZIP} \
     / lift ${VERBOSE} \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --output-file ${DATADIR}/all.node1.entity.counts.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --input-file-is-presorted \
     --label-file-is-presorted \
     --use-mgzip ${USE_MGZIP} \
     |& tee ${LOGDIR}/all.node1.entity.counts.log

echo -e "\nCount the entities in the label column in ${DATADIR}/all.${SORTED_KGTK} and lift English labels."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file ${DATADIR}/all.${SORTED_KGTK} \
     -p '; ^[PQ][^-]*$ ;' -o - \
     / unique ${VERBOSE} \
     --column label \
     --label label-entity-count \
     --use-mgzip ${USE_MGZIP} \
     / lift ${VERBOSE} \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --output-file ${DATADIR}/all.label.entity.counts.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --input-file-is-presorted \
     --label-file-is-presorted \
     --use-mgzip ${USE_MGZIP} \
     |& tee ${LOGDIR}/all.label.entity.counts.log

echo -e "\nCount the entities in the node2 column in ${DATADIR}/all.${SORTED_KGTK} and lift English labels."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file ${DATADIR}/all.${SORTED_KGTK} \
     -p ';; ^[PQ][^-]*$' -o - \
     / unique ${VERBOSE} \
     --column node2 \
     --label node2-entity-count \
     --use-mgzip ${USE_MGZIP} \
     / lift ${VERBOSE} \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --output-file ${DATADIR}/all.node2.entity.counts.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --input-file-is-presorted \
     --label-file-is-presorted \
     --use-mgzip ${USE_MGZIP} \
     |& tee ${LOGDIR}/all.node2.entity.counts.log
