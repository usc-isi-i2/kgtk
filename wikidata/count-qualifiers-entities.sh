#! /bin/bash

source common.sh

# ==============================================================================
echo -e "\nCount the entities in the node1 column in ${DATADIR}/qualifiers.${SORTED_KGTK} and lift English labels."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} --use-mgzip=${USE_MGZIP} --presorted \
     --input-file ${DATADIR}/qualifiers.${SORTED_KGTK} \
     --column node1 \
     --label node1-entity-count \
     / lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --output-file ${DATADIR}/qualifiers.node1.entity.counts.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --input-file-is-presorted \
     --label-file-is-presorted \
     |& tee ${LOGDIR}/qualifiers.node1.entity.counts.log

echo -e "\nCount the entities in the label column in ${DATADIR}/qualifiers.${SORTED_KGTK} and lift English labels."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE}  --use-mgzip=${USE_MGZIP} \
     --input-file ${DATADIR}/qualifiers.${SORTED_KGTK} \
     --column label \
     --label label-entity-count \
     / lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --output-file ${DATADIR}/qualifiers.label.entity.counts.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --input-file-is-presorted \
     --label-file-is-presorted \
     |& tee ${LOGDIR}/qualifiers.label.entity.counts.log

echo -e "\nCount the entities in the node2 column in ${DATADIR}/qualifiers.${SORTED_KGTK} and lift English labels."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file ${DATADIR}/qualifiers.${SORTED_KGTK} \
     -p ';; ^[PQ].*$' -o - \
     / unique ${VERBOSE}  --use-mgzip=${USE_MGZIP} \
     --column node2 \
     --label node2-entity-count \
     / lift ${VERBOSE}  --use-mgzip=${USE_MGZIP} \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --output-file ${DATADIR}/qualifiers.node2.entity.counts.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --input-file-is-presorted \
     --label-file-is-presorted \
     |& tee ${LOGDIR}/qualifiers.node2.entity.counts.log
